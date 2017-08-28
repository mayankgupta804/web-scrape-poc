from config.properties import Properties
from rabbitmq.connect import get_rabbit_mq_channel
from spiders.spider import Spider
from utility.counter import Counter
from utility.driver_wrapper import WebDriverWrapper
from utility.image_checker import *
from utility.logger import Logger
from utility.spell_checker import CheckWords
from utility.url import Url


class HeadlessSpider(Spider):
    config = ""
    device = ""
    image_check = False
    spell_check = False

    def __init__(self, base_url, domain_name, mongod):
        Spider.__init__(self, base_url, domain_name, mongod)
        HeadlessSpider.device = Properties.device
        HeadlessSpider.image_check = Properties.image_check
        HeadlessSpider.spell_check = Properties.spell_check
        self.crawl_page('First spider', Url(Spider.base_url), 0, get_rabbit_mq_channel())
        Counter.url += 1
        if self.image_check:
            ImageChecker(mongod).start()
        if self.spell_check:
            CheckWords(Spider.spelling_file, mongod).start()

    @classmethod
    def gather_links(cls, page_url):
        Logger.logger.info("gathering links " + page_url)
        try:
            with WebDriverWrapper(page_url, cls.device, cls.mongod) as driver:
                links = set(driver.get_all_links())
                img_links = set(driver.get_image_links())
                driver.is_blank_page()
                driver.add_words_to_queue()
        except Exception as e:
            Logger.logger.error(page_url + "\n" + str(e))
            print(str(e))
            return set()
        if cls.image_check:
            add_images_to_queue(img_links)
        return links
