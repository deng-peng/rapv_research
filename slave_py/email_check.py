from email.utils import parseaddr
from helper import *


class EmailCheck(object):
    def __init__(self):
        self.token = ''
        self.account = ''
        self.token_expire = ''
        self.url = 'https://api.linkedin.com/v1/people/email={}:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'
        self.proxies = {'https': "socks5://127.0.0.1:9050"}
        self.check_count = 0

    def check(self, email, header):
        self.check_count += 1
        # check email address valid
        if '@' not in parseaddr(email)[1]:
            return {'status': 400, 'message': 'invalid email address'}
        try:
            r = requests.get(self.url.format(email.replace('@', '%40')), headers=header, proxies=self.proxies,
                             timeout=30)
        except Exception, e:
            logging.warning(e)
            return False
        
        try:
            js = r.json()
            res = {}
            if 'errorCode' in js:
                if js['errorCode'] == 0:
                    if js['status'] == 401:
                        # u'errorCode': 0, u'status': 401, u'message': u'[unauthorized]. token expired 4803 seconds ago'
                        header['oauth_token'] = self.get_token(True)
                        return False
                    elif js['status'] == 500:
                        # u'errorCode': 0, u'status': 500, u'message': u'Internal service error'
                        header['oauth_token'] = self.get_token(True)
                        return False
                    elif js['status'] == 403 and 'Throttle limit' in js['message']:
                        header['oauth_token'] = self.get_token(True)
                        return False
                    else:
                        print js
                        res['errorCode'] = js['errorCode']
                        res['status'] = js['status']
                        res['message'] = js['message']
                        return res
            elif 'publicProfileUrl' in js:
                res['publicProfileUrl'] = js['publicProfileUrl']
                # public profile url
                res['status'] = 200
                return res
            elif 'siteStandardProfileRequest' in js:
                res['publicProfileUrl'] = js['siteStandardProfileRequest']['url']
                # encoded profile url
                res['status'] = 201
                return res
            else:
                print js
                return False
        except Exception, e:
            print(e)
            logging.warning(e)
            logging.warning(r.text)
            return False

    def make_header(self):
        header = {
            'x-requested-with': 'IN.XDCall',
            'x-li-format': 'json',
            'x-http-method-override': 'GET',
            'x-cross-domain-origin': 'https://mail.google.com',
            'content-type': 'application/json',
            'user-agent': Helper.get_user_agent(),
            'oauth_token': self.get_token()
        }
        return header

    def get_token(self, force=False):
        if force:
            self.token = ''
            self.set_account_status('frozen')
        else:
            if self.token != '':
                if self.token_expire > time.time():
                    return self.token
                else:
                    self.token = self.__renew_token(self.account)
                    return self.token
        self.token = self.inner_get_token()
        return self.token

    def set_account_status(self, status):
        try:
            requests.post(account_url + '/api/slave/cookie', data={'account': self.account, 'status': status})
        except Exception, e:
            logging.warning(threading.currentThread().name)
            logging.warning(e)

    @retry(wait_fixed=90000)
    def inner_get_token(self):
        r = requests.get(account_url + '/api/slave/cookie')
        if r.text == '':
            Helper.report_slave_running_status('waiting', self.check_count)
            raise Exception('waiting for active account')
        else:
            js = r.json()
            self.account = js['account']
            self.token = self.__renew_token(self.account)
            if len(self.token) > 0:
                self.token_expire = time.time() + 1800 - 60 * 1
                print '{0} token changed : {1}'.format(threading.currentThread().name, self.token)
                Helper.report_slave_running_status('working', self.check_count)
                return self.token
            else:
                self.set_account_status('invalid')
                raise Exception('invalid account')

    def __renew_token(self, account):
        try:
            headers = {'cookie': 'li_at=' + account, 'referer': 'https://mail.google.com/mail/u/0/'}
            r = requests.get(
                'https://www.linkedin.com/uas/js/userspace?v=0.0.2000-RC8.55927-1429&apiKey={0}&onLoad=linkedInAPILoaded{0}&authorize=true&credentialsCookie=true&secure=1&'.format(
                    '4XZcfCb3djUl-DHJSFYd1l0ULtgSPl9sXXNGbTKT2e003WAeT6c2AqayNTIN5T1s',
                    random.randint(100000000000000, 999999999999999)),
                headers=headers, proxies=self.proxies)
            origin = r.text.find('l.oauth_token')
            start = r.text.find('"', origin)
            end = r.text.find('"', start + 1)
            token = r.text[start + 1:end]
            return token
        except Exception, e:
            logging.warning(threading.currentThread().name)
            logging.warning(e)
            return ''

    @retry
    def get_proxy(self):
        r = requests.get(master_url + '/proxy')
        js = r.json()
        proxy_id = js['id']
        host = js['host']
        port = js['port']
        protocol = js['protocol'].lower()
        if Helper.is_proxy_valid(protocol, host, port):
            return {'https': "{0}://{1}:{2}".format(protocol, host, port)}
        else:
            Helper.update_proxy_status(proxy_id, 'invalid')
            raise Exception('invalid proxy')
