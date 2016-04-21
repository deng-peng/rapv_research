from __init__ import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TokenMake(object):
    def __init__(self):
        self.account = ''
        self.password = ''
        self.get_account()

    def make(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch',
            'referer': 'http://www.linkedin.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        for key, value in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
        driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=uno-reg-guest-home')

        # login user
        email = driver.find_element_by_id("session_key-login")
        email.send_keys(self.account)
        password = driver.find_element_by_id("session_password-login")
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.save_screenshot('{0}-{1}.png'.format(self.account, time.time()))

        driver.get('http://rapportive.jelzo.com:8080/token.html')
        token = driver.execute_script('return IN.ENV.auth.oauth_token')
        return token

    def get_account(self):
        while True:
            r = requests.get(master_url + '/account')
            if r.text == '':
                print 'no active account exist, retry in 60 seconds'
                time.sleep(60)
            else:
                js = r.json()
                self.account = js['account']
                self.password = js['password']
                print 'account changed : {0}'.format(self.account)
                break
