from __init__ import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Factory
from pyvirtualdisplay import Display


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
        driver.quit()
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
        # ignore register new
        time.sleep(3600 * 2)
        return

        display = Display(visible=0, size=(800, 600))
        display.start()

        fake = Factory.create()
        years = range(1970, 2015)
        first = fake.first_name()
        last = fake.last_name()
        email = '{0}{1}{2}@{3}'.format(first, last, random.choice(years), fake.domain_name())
        print 'register new account {0}'.format(email)
        password = default_linkedin_password

        driver = webdriver.Chrome()
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

        if 'start/join' in driver.current_url:
            if 'security check' in driver.page_source or 'Security verification' in driver.page_source:
                countries = driver.find_elements_by_css_selector('#country-select option')
                if len(countries) > 0:
                    try:
                        driver.find_element_by_css_selector('#country-select option[value=cn]').click()
                        time.sleep(1)
                        phone_number = driver.find_element_by_id('phoneNumber')
                        phone_number.send_keys('13800138000')
                        phone_number.send_keys(Keys.RETURN)
                        time.sleep(10)
                        if driver.find_element_by_css_selector('.toast.success').is_displayed():
                            challenge = driver.find_element_by_id('challenge-input')
                            challenge.send_keys('123456')
                            challenge.send_keys(Keys.RETURN)
                    except Exception, e:
                        driver.save_screenshot('./screenshots/debug-{0}-{1}.png'.format(self.account, time.time()))
                        print e

        if 'start/join' not in driver.current_url:
            if 'security check' not in driver.page_source and 'Security verification' not in driver.page_source:
                # save account to master
                requests.post(master_url + '/account', data={'account': email, 'password': password})

                driver.save_screenshot('./screenshots/{0}-{1}.png'.format(self.account, time.time()))

                # get token for new account
                driver.get('http://rapportive.jelzo.com:8080/token.html')
                self.token = driver.execute_script('return IN.ENV.auth.oauth_token')

        driver.quit()
        display.stop()
        # stop script if can't get token
        if self.token == '':
            print 'could not get token, sleep 1 hours'
            time.sleep(3600 * 2)
