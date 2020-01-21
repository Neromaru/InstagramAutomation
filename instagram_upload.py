import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pynput.keyboard import Key, Controller

from image_formatter import create_post


class InstagramUploader:
    # Emulate mobile from a Google Chrome
    mobile_emulation = {

        "deviceMetrics": {
            "width": 360, "height": 640, "pixelRatio": 3.0
        },
        "userAgent":
            "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) \
             AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    def __init__(self, username, password, file_path):
        self.keybord = Controller()
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,
                                       executable_path=os.path.join(os.path.curdir, 'chromedriver')
                                       )
        self.path = file_path
        self.username = username
        self.password = password
        self.login_page = "https://www.instagram.com/accounts/login/"

    def _run(self):
        self._login()
        image, post = create_post(self.path)
        self._create_new_post(image, post)
        os.remove(image)

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

    def _create_new_post(self, image, text):
        # close popups of Instagram
        if self.wait_for(By.CLASS_NAME, 'GAMXX'):
            self.driver.find_element_by_xpath('//main/div/button').click()
        if self.wait_for(By.CLASS_NAME, 'HoLwm'):
            self.driver.find_element_by_class_name('HoLwm').click()

        inputs = self.driver.find_elements_by_xpath('//input[@type="file"]')
        poster = self.driver.find_element_by_xpath('//span[@aria-label="New Post"]')
        poster.click()

        # Pass file to needed inputs
        for input in inputs:
            try:
                input.send_keys(image)
            except StaleElementReferenceException:
                continue
        # This is done to close the open file window
        self.keybord.press(Key.esc)
        self.keybord.release(Key.esc)

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
        return self._run()
