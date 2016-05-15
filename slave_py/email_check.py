from __init__ import *
from email.utils import parseaddr


class EmailCheck(object):
    def __init__(self):
        self.token = ''
        self.account = ''
        self.token_expire = ''
        self.url = 'https://api.linkedin.com/v1/people/email={}:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'

    def check(self, email, header):
        try:
            # check email address valid
            if '@' not in parseaddr(email)[1]:
                return {'status': 400, 'message': 'invalid email address'}
            r = requests.get(self.url.format(email.replace('@', '%40')), headers=header, timeout=30)
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
            'user-agent': self.__make_user_agent(),
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
        requests.post(account_url + '/api/slave/cookie', data={'account': self.account, 'status': status})

    @staticmethod
    def report_slave_running_status(status):
        requests.post(master_url + '/slave/status', data={'status': status})

    def inner_get_token(self):
        while True:
            r = requests.get(account_url + '/api/slave/cookie')
            if r.text == '':
                print 'waiting for active account'
                self.report_slave_running_status('waiting')
                time.sleep(90)
            else:
                js = r.json()
                self.account = js['account']
                self.token = self.__renew_token(self.account)
                if len(self.token) > 0:
                    self.token_expire = time.time() + 1800 - 60 * 1
                    print 'token changed : ' + self.token
                    self.report_slave_running_status('working')
                    return self.token
                else:
                    self.set_account_status('invalid')

    @staticmethod
    def __renew_token(account):
        headers = {'cookie': 'li_at=' + account, 'referer': 'https://mail.google.com/mail/u/0/'}
        r = requests.get(
            'https://www.linkedin.com/uas/js/userspace?v=0.0.2000-RC8.55927-1429&apiKey={0}&onLoad=linkedInAPILoaded{0}&authorize=true&credentialsCookie=true&secure=1&'.format(
                '4XZcfCb3djUl-DHJSFYd1l0ULtgSPl9sXXNGbTKT2e003WAeT6c2AqayNTIN5T1s',
                random.randint(100000000000000, 999999999999999)),
            headers=headers)
        origin = r.text.find('l.oauth_token')
        start = r.text.find('"', origin)
        end = r.text.find('"', start + 1)
        token = r.text[start + 1:end]
        return token

    @staticmethod
    def __make_user_agent():
        return random.choice([
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
            'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        ])
