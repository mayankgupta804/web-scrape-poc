from config.properties import Properties
from rabbitmq.connect import get_rabbit_mq_channel
from spiders.spider import Spider
from utility.driver_wrapper import WebDriverWrapper
from utility.image_checker import *
from utility.logger import Logger
from utility.spell_checker import CheckWords


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
        self.crawl_page('First spider', Spider.base_url, 0, get_rabbit_mq_channel())
        if self.image_check:
            ImageChecker(mongod).start()
        if self.spell_check:
            CheckWords(Spider.spelling_file, mongod).start()

    @classmethod
    def crawl_page(cls, thread_name, page_url, depth, channel):
        super().crawl_page(thread_name, page_url, depth, channel)

    @classmethod
    def gather_links(cls, page_url):
        Logger.logger.info("gathering links " + page_url)
        try:
            with WebDriverWrapper(page_url, cls.device, cls.mongod) as driver:
                links = driver.get_all_links()
                img_links = driver.get_image_links()
                driver.is_blank_page()
                driver.add_words_to_queue()
        except Exception as e:
            Logger.logger.error(page_url + "\n" + str(e))
            print(str(e))
            return set()
        if cls.image_check:
            add_images_to_queue(img_links)
        return links

    @classmethod
    def add_links_to_queue(cls, links, depth, channel, thread_name):
        super().add_links_to_queue(links, depth, channel, thread_name)
