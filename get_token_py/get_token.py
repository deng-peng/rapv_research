import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from get_token_py import account

service_args = [
    # '--proxy=127.0.0.1:1080',
    # '--proxy-type=socks5',
    # '--proxy-type=http',
]
# driver = webdriver.PhantomJS(service_args=service_args)
driver = webdriver.Chrome(service_args=service_args)
driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=uno-reg-guest-home')

# login user
email = driver.find_element_by_id("session_key-login")
email.send_keys(account.linkedin_account)
password = driver.find_element_by_id("session_password-login")
password.send_keys(account.linkedin_password)
password.send_keys(Keys.RETURN)
time.sleep(3)

driver.get('http://rapportive.jelzo.com/token.html')
token = driver.execute_script('return IN.ENV.auth.oauth_token')
print token
