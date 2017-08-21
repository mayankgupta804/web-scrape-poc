from config.properties import Properties
from rabbitmq.connect import get_rabbit_mq_channel
from utility.image_checker import *
from utility.link_finder import LinkFinder
from utility.logger import Logger
from utility.spell_checker import CheckWords
from utility.utilities import append_to_file

from utility.driver_wrapper import WebDriverWrapper
from config.property_reader import PropertyReader
from spiders.spider import Spider


class HeadlessSpider(Spider):
    config = ""
    device = ""
    image_check = False
    spell_check = False

    def __init__(self, base_url, domain_name, mongod):
        Spider.__init__(self, base_url, domain_name, mongod)
        # Spider.boot()
        HeadlessSpider.device = Properties.device
        HeadlessSpider.image_check = Properties.image_check
        HeadlessSpider.spell_check = Properties.spell_check
        self.crawl_page('First spider', Spider.base_url, 0, get_rabbit_mq_channel())
        if self.image_check:
            ImageChecker(Spider.broken_images_file).start()
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
                html_string = driver.get_page_source()
                driver.is_blank_page()
                driver.add_words_to_queue()
            finder = LinkFinder(cls.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            Logger.logger.error(page_url + "\n" + str(e))
            print(str(e))
            return set()
        if cls.image_check:
            add_images_to_queue(finder.image_links())
        return finder.page_links()

    @classmethod
    def add_links_to_queue(cls, links, depth, channel, thread_name):
        super().add_links_to_queue(links, depth, channel, thread_name)
