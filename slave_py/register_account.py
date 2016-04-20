from __init__ import *
from faker import Factory
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

fake = Factory.create()
years = range(1970, 2015)
first = fake.first_name()
last = fake.last_name()
email = '{0}{1}{2}@{3}'.format(first, last, random.choice(years), fake.domain_name())
print email
password = default_linkedin_password

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch',
    'referer': 'http://www.linkedin.com/',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
}
for key, value in enumerate(headers):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
driver = webdriver.PhantomJS(service_args=['--ssl-protocol=any'])
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
time.sleep(3)
requests.post(master_url + '/account', data={'account': email})
