from __init__ import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TokenMake(object):
    def __init__(self):
        self.account = ''
        self.password = ''
        self.get_account()

    def make(self):
        driver = webdriver.PhantomJS()
        driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=uno-reg-guest-home')

        # login user
        email = driver.find_element_by_id("session_key-login")
        email.send_keys(self.account)
        password = driver.find_element_by_id("session_password-login")
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

        driver.get('http://rapportive.jelzo.com/token.html')
        token = driver.execute_script('return IN.ENV.auth.oauth_token')
        return token

    def get_account(self):
        r = requests.get(master_url + '/account')
        if r.text == '':
            print 'no active account exist, retry in 60 seconds'
            time.sleep(60)
            self.get_account()
        else:
            js = r.json()
            self.account = js['account']
            self.password = js['password']
