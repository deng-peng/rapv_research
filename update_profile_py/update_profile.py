import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import account

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/uas/login')

# login user
email = driver.find_element_by_id("session_key-login")
email.send_keys(account.linkedin_account)
password = driver.find_element_by_id("session_password-login")
password.send_keys(account.linkedin_password)
password.send_keys(Keys.RETURN)
time.sleep(3)

# profiel
driver.get('http://www.linkedin.com/profile/edit?trk=hp-identity-edit-profile')
# name
driver.find_element_by_css_selector('#name > h1 > button').click()
time.sleep(1)
driver.find_element_by_css_selector('#firstName-editNameForm').clear()
driver.find_element_by_css_selector('#firstName-editNameForm').send_keys('Steve')
time.sleep(1)
driver.find_element_by_css_selector('#lastName-editNameForm').clear()
driver.find_element_by_css_selector('#lastName-editNameForm').send_keys('Dickens')
time.sleep(1)
driver.find_element_by_css_selector('#name-edit > p > input').click()
time.sleep(5)

# headline
# driver.find_element_by_css_selector('#headline > div.field > button').click()
# driver.find_element_by_css_selector('#headline-editHeadlineForm').click()
# driver.find_element_by_css_selector('#headline-edit > p.actions > input').click()

# country
driver.find_element_by_css_selector('#location > div.field > button').click()
time.sleep(1)
select = Select(driver.find_element_by_css_selector('#countryCode-location-editLocationForm'))
select.deselect_all()
select.select_by_visible_text("Australia")
time.sleep(1)
driver.find_element_by_css_selector('#postalCode-location-editLocationForm').send_keys('2000')
time.sleep(1)
select = Select(driver.find_element_by_css_selector('#industryChooser-editLocationForm'))
select.deselect_all()
select.select_by_visible_text("Internet")
time.sleep(1)
driver.find_element_by_css_selector('form[name=editLocationForm] > p > input').click()
time.sleep(3)

# current job
driver.find_element_by_css_selector('.recommended-section-experience > .recommended-section-add').click()
time.sleep(1)
# company name
driver.find_element_by_css_selector('#companyName-positionCompany-position-editPositionForm').send_keys('contact master')
time.sleep(1)
# title
driver.find_element_by_css_selector('#title-position-editPositionForm').send_keys('manager')
# time period
select = Select(driver.find_element_by_css_selector('#month-startDate-position-editPositionForm'))
select.deselect_all()
select.select_by_visible_text("May")
driver.find_element_by_css_selector('#year-startDate-position-editPositionForm').clear()
driver.find_element_by_css_selector('#year-startDate-position-editPositionForm').send_keys('2012')
driver.find_element_by_css_selector('#isCurrent-endDate-position-editPositionForm').click()
driver.find_element_by_css_selector('form[name=editPositionForm] > p > input').click()
