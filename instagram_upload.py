from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class InstagraUploader:
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

    def __init__(self, username, password):

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options,
                                       executable_path='/home/vadym/PycharmProjects/instagram/chromedriver')
        # self.path = file_path
        self.username = username
        self.password = password
        self.login_page = "https://www.instagram.com/accounts/login/"

    def _run(self):
        self._login()
        self._create_new_post()

    def wait_for(self, by, value):
        delay = 6
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((by, value)))
            print "Page is ready!"
        except TimeoutException:
            print "Loading took too much time!"

    def _login(self):
        self.driver.get(self.login_page)
        self.wait_for(By.NAME, 'username')
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        submit = self.driver.find_element_by_xpath('//button[@type="submit"]')
        username.send_keys(self.username)
        password.send_keys(self.password)
        submit.click()

    def _create_new_post(self):
        self.wait_for(By.CLASS_NAME, 'GAMXX')
        self.driver.find_element_by_xpath('//main/div/button').click()
        self.wait_for(By.CLASS_NAME, 'HoLwm')
        self.driver.find_element_by_class_name('HoLwm').click()
        poster = self.driver.find_element_by_xpath('//span[@aria-label="New Post"]')
        poster.click()
        print "Hi!"
