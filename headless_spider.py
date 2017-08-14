from driver_wrapper import WebDriverWrapper
from image_checker import *
from link_finder import LinkFinder
from properties import Properties
from spell_check import CheckWords
from spider import Spider
from utilities import append_to_file


class HeadlessSpider(Spider):
    config = ""
    device = ""

    def __init__(self, config, base_url, domain_name):
        Spider.__init__(self, config, base_url, domain_name)
        Spider.boot(config)
        HeadlessSpider.config = config
        HeadlessSpider.device = Properties(config).device
        self.crawl_page('First spider', (Spider.base_url, 0))
        ImageChecker(Spider.broken_images_file).start()
        CheckWords(Spider.spelling_file).start()

    @classmethod
    def crawl_page(cls, thread_name, page_url):
        super().crawl_page(thread_name, page_url)

    @classmethod
    def gather_links(cls, page_url):
        try:
            with WebDriverWrapper(page_url, cls.device) as driver:
                html_string = driver.get_page_source()
                driver.add_words_to_queue()
            finder = LinkFinder(cls.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            append_to_file(Properties(cls.config).error_file, page_url + "\n" + str(e))
            print(str(e))
            return set()
        add_images_to_queue(finder.image_links())
        return finder.page_links()

    @classmethod
    def add_links_to_queue(cls, links, depth):
        super().add_links_to_queue(links, depth)

    @classmethod
    def update_files(cls):
        super().update_files()
