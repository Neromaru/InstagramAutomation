import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options, FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from image_formatter import create_post

skip_profile = 2


def caps():
    profile = FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1")
    profile.set_preference("intl.accept_languages", 'en-us')
    return profile


class InstagramUploader:
    # Emulate mobile from a Firefox

    options = Options()
    options.headless = False

    def __init__(self, username, password, file_path):
        self.driver = webdriver.Firefox(options=self.options,
                                        firefox_profile=caps(),
                                        executable_path=os.path.join(
                                            os.path.curdir, 'geckodriver'),
                                        )
        self.driver.implicitly_wait(3)
        self.path = file_path
        self.username = username
        self.password = password
        self.login_page = "https://www.instagram.com/accounts/login/"

    def _run(self):
        self._login()
        image, post = create_post(self.path)
        self._create_new_post(image, post)
        os.remove(image)
        self.driver.close()

    def wait_for(self, by, value):
        """
        This function implements waiting for an element
        """
        delay = 6
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False

    def _login(self):
        self.driver.get(self.login_page)
        self.wait_for(By.NAME, 'username')

        # Find form elements
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        submit = self.driver.find_element_by_xpath('//button[@type="submit"]')

        # Pass credentials
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def find_poster(self):
        svgs = self.driver.find_elements_by_tag_name('svg')
        for element in svgs:
            label = element.get_attribute('aria-label') == 'New Post'
            if label:
                return element
        raise NoSuchElementException

    def _create_new_post(self, image, text):
        time.sleep(2)
        # close popups of Instagram
        if self.wait_for(By.CLASS_NAME, 'GAMXX'):
            self.driver.find_element_by_xpath('//main/div/button').click()
        if self.wait_for(By.CLASS_NAME, 'HoLwm'):
            self.driver.find_element_by_class_name('HoLwm').click()

        inputs = self.driver.find_elements_by_xpath('//input[@type="file"]')

        poster = self.find_poster()
        poster.click()
        # Pass file to needed inputs

        for input in inputs[skip_profile:]:
            try:
                input.send_keys(image)
            except StaleElementReferenceException:
                continue

        # Set active window of browser instead of file browser
        self.wait_for(By.CLASS_NAME, "UP43G")
        self.driver.find_element_by_xpath('//button[@class="UP43G"]').click()

        # Inputs fields
        if self.wait_for(By.TAG_NAME, "textarea"):
            self.driver.find_element_by_tag_name('textarea').send_keys(text)

        # Publishing button
        if self.wait_for(By.CLASS_NAME, "UP43G"):
            self.driver.find_element_by_xpath('//button[@class="UP43G"]').click()

    def run(self):
        try:
            return self._run()
        finally:
            self.driver.close()
