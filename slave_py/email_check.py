from __init__ import *
from email.utils import parseaddr
from helper import *


class EmailCheck(object):
    def __init__(self):
        self.token = ''
        self.account = ''
        self.token_expire = ''
        self.url = 'https://api.linkedin.com/v1/people/email={}:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'
        self.proxies = {}

    def check(self, email, header):
        try:
            # check email address valid
            if '@' not in parseaddr(email)[1]:
                return {'status': 400, 'message': 'invalid email address'}
            r = requests.get(self.url.format(email.replace('@', '%40')), headers=header, proxies=self.proxies,
                             timeout=30)
            js = r.json()
            print js
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
                return False
        except requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError:
            self.proxies = self.get_proxy()
            return False
        except Exception, e:
            print(e)
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
        self.proxies = self.get_proxy()
        return self.token

    def set_account_status(self, status):
        requests.post(account_url + '/api/slave/cookie', data={'account': self.account, 'status': status})

    @retry(wait_fixed=90000)
    def inner_get_token(self):
        r = requests.get(account_url + '/api/slave/cookie')
        if r.text == '':
            Helper.report_slave_running_status('waiting')
            raise Exception('waiting for active account')
        else:
            js = r.json()
            self.account = js['account']
            self.token = self.__renew_token(self.account)
            if len(self.token) > 0:
                self.token_expire = time.time() + 1800 - 60 * 1
                print '{0} token changed : {1}'.format(threading.currentThread().name, self.token)
                Helper.report_slave_running_status('working')
                return self.token
            else:
                self.set_account_status('invalid')
                raise Exception('invalid account')

    def __renew_token(self, account):
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

    @retry
    def get_proxy(self):
        r = requests.post(master_url + '/proxy')
        proxy_str = r.text.strip()
        if Helper.is_proxy_valid(proxy_str):
            return {'https': "socks5://" + proxy_str}
        else:
            Helper.post_proxy_status(proxy_str, False)
            raise Exception('invalid proxy')
