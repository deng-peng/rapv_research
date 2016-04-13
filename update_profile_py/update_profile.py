import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import account
import read_profile_data


class LinkedinProfile:
    def __init__(self):
        service_args = [
            # '--proxy=127.0.0.1:1080',
            # '--proxy-type=socks5',
        ]
        self.driver = webdriver.Chrome(service_args=service_args)
        self.profile = None

    def login(self):
        self.driver.get('https://www.linkedin.com/uas/login')
        # login user
        email = self.driver.find_element_by_id("session_key-login")
        email.send_keys(account.linkedin_account)
        password = self.driver.find_element_by_id("session_password-login")
        password.send_keys(account.linkedin_password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def load_profile(self):
        maker = read_profile_data.ProfileMaker()
        self.profile = maker.make()

    def set_profile(self):
        # profiel
        self.driver.get('http://www.linkedin.com/profile/edit?trk=hp-identity-edit-profile')
        time.sleep(3)
        # name
        self.driver.find_element_by_css_selector('#name > h1 > button').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('#firstName-editNameForm').clear()
        self.driver.find_element_by_css_selector('#firstName-editNameForm').send_keys(self.profile.given_name)
        time.sleep(1)
        self.driver.find_element_by_css_selector('#lastName-editNameForm').clear()
        self.driver.find_element_by_css_selector('#lastName-editNameForm').send_keys(self.profile.family_name)
        time.sleep(1)
        self.driver.find_element_by_css_selector('#name-edit > p > input').click()
        time.sleep(5)

        # headline
        self.driver.find_element_by_css_selector('#headline > div.field > button').click()
        self.driver.find_element_by_css_selector('#headline-editHeadlineForm').clear()
        self.driver.find_element_by_css_selector('#headline-editHeadlineForm').send_keys(
            '{0} at {1}'.format(self.profile.title, self.profile.organization))
        self.driver.find_element_by_css_selector('#headline-edit > p.actions > input').click()
        time.sleep(3)

        # country
        self.driver.find_element_by_css_selector('#location > div.field > button').click()
        time.sleep(1)
        select = Select(self.driver.find_element_by_css_selector('#countryCode-location-editLocationForm'))
        select.select_by_visible_text("Australia")
        # select.select_by_visible_text("United States")
        time.sleep(1)
        self.driver.find_element_by_css_selector('#postalCode-location-editLocationForm').clear()
        self.driver.find_element_by_css_selector('#postalCode-location-editLocationForm').send_keys('2000')
        # self.driver.find_element_by_css_selector('#postalCode-location-editLocationForm').send_keys('10000')
        time.sleep(1)
        select = Select(self.driver.find_element_by_css_selector('#industryChooser-editLocationForm'))
        select.select_by_visible_text(self.profile.industry)
        time.sleep(1)
        self.driver.find_element_by_css_selector('form[name=editLocationForm] > p > input').click()
        time.sleep(3)

        self.set_photo()
        self.set_experience()

    def set_photo(self):
        try:
            self.driver.find_element_by_css_selector('.edit-photo-content').click()
            time.sleep(3)
            photo_path = random.choice(account.photo)
            self.driver.find_element_by_css_selector('.photo-uploader form > input[type="file"]').send_keys(photo_path)
            time.sleep(3)
            self.driver.find_element_by_css_selector('button.save').click()
        except NoSuchElementException, ne:
            print ne
        if len(self.driver.find_elements_by_css_selector('button.cancel')) > 0:
            self.driver.find_element_by_css_selector('button.cancel').click()

    def set_experience(self):
        if len(self.driver.find_elements_by_css_selector(
                '.recommended-section-experience > .recommended-section-add')) > 0:
            self.driver.find_element_by_css_selector(
                '.recommended-section-experience > .recommended-section-add').click()
        elif len(self.driver.find_elements_by_css_selector('#background-experience > button')) > 0:
            self.driver.find_element_by_css_selector('#background-experience > button').click()
        else:
            return False
        time.sleep(1)
        # company name
        self.driver.find_element_by_css_selector('#companyName-positionCompany-position-editPositionForm').send_keys(
            self.profile.organization)
        time.sleep(1)
        # title
        self.driver.find_element_by_css_selector('#title-position-editPositionForm').send_keys(self.profile.title)
        # time period
        select = Select(self.driver.find_element_by_css_selector('#month-startDate-position-editPositionForm'))
        select.select_by_visible_text(self.profile.start_month)
        self.driver.find_element_by_css_selector('#year-startDate-position-editPositionForm').clear()
        self.driver.find_element_by_css_selector('#year-startDate-position-editPositionForm').send_keys(
            self.profile.start_year)
        self.driver.find_element_by_css_selector('#isCurrent-endDate-position-editPositionForm').click()
        self.driver.find_element_by_css_selector('#summary-position-editPositionForm').send_keys(
            self.profile.description)
        self.driver.find_element_by_css_selector('form[name=editPositionForm] > p > input').click()

    def save_screen(self):
        self.driver.save_screenshot(account.linkedin_account + '.png')


if __name__ == '__main__':
    profile = LinkedinProfile()
    profile.load_profile()
    try:
        profile.login()
        profile.set_profile()
    except Exception, e:
        print e
        profile.save_screen()
