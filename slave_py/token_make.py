from __init__ import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Factory


class TokenMake(object):
    def __init__(self):
        self.account = ''
        self.password = ''
        self.token = ''
        screenshots = os.getcwd() + '/screenshots/'
        if not os.path.exists(screenshots):
            os.mkdir(screenshots)

    def make(self):
        self.get_account()
        if len(self.token) > 0:
            return self.token

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
        driver.save_screenshot('./screenshots/{0}-{1}.png'.format(self.account, time.time()))

        driver.get('http://rapportive.jelzo.com:8080/token.html')
        token = driver.execute_script('return IN.ENV.auth.oauth_token')
        return token

    def get_account(self):
        r = requests.get(master_url + '/account')
        if r.text == '':
            self.register()
        else:
            js = r.json()
            self.account = js['account']
            self.password = js['password']
            print 'account changed : {0}'.format(self.account)

    def register(self):
        fake = Factory.create()
        years = range(1970, 2015)
        first = fake.first_name()
        last = fake.last_name()
        email = '{0}{1}{2}@{3}'.format(first, last, random.choice(years), fake.domain_name())
        print 'register new account {0}'.format(email)
        password = default_linkedin_password

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, sdch',
            'referer': 'http://www.linkedin.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }
        for key, value in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        service_args = [
            # '--proxy=182.254.153.54:8080',
            # '--proxy-type=http',
            '--ssl-protocol=any'
        ]
        driver = webdriver.PhantomJS(service_args=service_args)
        driver.get('https://www.linkedin.com')
        driver.add_cookie(
            {u'domain': u'.linkedin.com', u'name': u'lang', u'value': u'"v=2&lang=en-us&c="',
             u'path': u'/', u'httpOnly': False, u'secure': False})
        driver.get('https://www.linkedin.com/start/join?trk=hb_join')

        first_input = driver.find_element_by_id("first-name")
        first_input.send_keys(first)
        last_input = driver.find_element_by_id("last-name")
        last_input.send_keys(last)
        email_input = driver.find_element_by_id("join-email")
        email_input.send_keys(email)
        password_input = driver.find_element_by_id("join-password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)

        self.account = email
        self.password = password
        self.token = ''
        driver.save_screenshot('./screenshots/debug-{0}-{1}.png'.format(self.account, time.time()))

        print 'current url : {0}'.format(driver.current_url)

        if 'start/join' not in driver.current_url:
            if 'security check' not in driver.page_source and 'Security verification' not in driver.page_source:
                # save account to master
                requests.post(master_url + '/account', data={'account': email, 'password': password})

                driver.save_screenshot('./screenshots/{0}-{1}.png'.format(self.account, time.time()))

                # get token for new account
                driver.get('http://rapportive.jelzo.com:8080/token.html')
                self.token = driver.execute_script('return IN.ENV.auth.oauth_token')

        # stop script if can't get token
        if self.token == '':
            print 'could not get token, sleep 1 hours'
            time.sleep(3600 * 2)
