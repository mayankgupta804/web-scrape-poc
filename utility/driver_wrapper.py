import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.properties import Properties
from data.devices import device_mappings
from utility.spell_checker import *


class WebDriverWrapper:
    def __init__(self, page_url, device, mongod):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        if device is not None:
            mobile_emulation = device_mappings[device.lower()]
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        self._page_url = page_url
        self.mongod = mongod
        self._driver = webdriver.Chrome(executable_path=os.path.abspath("resources/chromedriver"),
                                        chrome_options=chrome_options)

    def __enter__(self):
        Logger.logger.info("opening with webdriver " + self._page_url)
        self._driver.get(self._page_url)
        self.page_source = self._driver.page_source
        return self

    def __exit__(self, *args):
        self._driver.quit()

    def get_page_source(self):
        return self.page_source

    def save_screenshot(self):
        return self._driver.save_screenshot(os.path.abspath(self._page_url + ".png"))

    def add_words_to_queue(self):
        add_words_to_queue(self._driver.find_element_by_tag_name('body').text, self._page_url)

    def is_blank_page(self):
        body = self._driver.find_element_by_tag_name("body").text
        if len(body) == 0:
            self.mongod.add_links_to_blank_page(self._page_url)

    def get_all_links(self):
        soup = BeautifulSoup(self.page_source, "html.parser")
        links = []
        for link in soup.findAll('a'):
            links.append(urljoin(Properties.home_page, link.get('href')))
        return filter(None, links)

    def get_image_links(self):
        soup = BeautifulSoup(self.page_source, "html.parser")
        links = []
        for img in soup.findAll('img'):
            link = img.get('src')
            if link and not link.startswith("data:image/svg"):
                links.append(urljoin(Properties.home_page, img.get('src')))
        return links
