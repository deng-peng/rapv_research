from __init__ import *
from slave_py.token_make import TokenMake


class EmailCheck(object):
    def __init__(self):
        self.token = ''
        self.token_expire = ''
        self.url = 'https://api.linkedin.com/v1/people/email={}:(first-name,last-name,headline,location,distance,positions,twitter-accounts,im-accounts,phone-numbers,member-url-resources,picture-urls::(original),site-standard-profile-request,public-profile-url,relation-to-viewer:(connections:(person:(first-name,last-name,headline,site-standard-profile-request,picture-urls::(original)))))'

    def check(self, email, header):
        try:
            r = requests.get(self.url.format(email.replace('@', '%40')), headers=header, timeout=30)
            js = r.json()
            print js
            res = {}
            if 'errorCode' in js:
                res['errorCode'] = js['errorCode']
                res['status'] = js['status']
                res['message'] = js['message']
                return res
            elif 'publicProfileUrl' in js:
                res['publicProfileUrl'] = js['publicProfileUrl']
                res['distance'] = js['distance']
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
        print 'current token : ' + self.token
        return header

    @staticmethod
    def __make_user_agent():
        return random.choice([
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',

        ])

    def get_token(self, force=False):
        if not force:
            if self.token != '' and self.token_expire < time.time():
                return self.token
        maker = TokenMake()
        self.token = maker.make()
        self.token_expire = time.time() + 1800 - 60 * 5
