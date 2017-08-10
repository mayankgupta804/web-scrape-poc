import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from spell_check import *


class WebDriverWrapper:
    def __init__(self, page_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        self._page_url = page_url
        self._driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)

    def __enter__(self):
        self._driver.get(self._page_url)
        return self

    def __exit__(self, *args):
        self._driver.close()

    def get_page_source(self):
        return self._driver.page_source

    def save_screenshot(self):
        return self._driver.save_screenshot(os.path.abspath(self._page_url + ".png"))

    def add_words_to_queue(self):
        add_words_to_queue(self._driver.find_element_by_tag_name('body').text, self._page_url)
