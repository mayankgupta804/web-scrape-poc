from utility.image_checker import *
from utility.link_finder import LinkFinder
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

    def __init__(self, config, base_url, domain_name,mongod):
        Spider.__init__(self, config, base_url, domain_name,mongod)
        Spider.boot(config)
        HeadlessSpider.config = config
        HeadlessSpider.device = PropertyReader(config).device
        HeadlessSpider.image_check = PropertyReader(config).image_check
        HeadlessSpider.spell_check = PropertyReader(config).spell_check
        self.crawl_page('First spider', (Spider.base_url, 0))
        if self.image_check:
            ImageChecker(Spider.broken_images_file).start()
        if self.spell_check:
            CheckWords(Spider.spelling_file).start()

    @classmethod
    def crawl_page(cls, thread_name, page_url):
        super().crawl_page(thread_name, page_url)

    @classmethod
    def gather_links(cls, page_url):
        try:
            with WebDriverWrapper(page_url, cls.device) as driver:
                html_string = driver.get_page_source()
                content = driver.get_body_text().text
                if len(content) == 0:
                    append_to_file(PropertyReader(cls.config).blank_pages_file, page_url)
                driver.add_words_to_queue()
            finder = LinkFinder(cls.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            append_to_file(PropertyReader(cls.config).error_file, page_url + "\n" + str(e))
            print(str(e))
            return set()
        if cls.image_check:
            add_images_to_queue(finder.image_links())
        return finder.page_links()

    @classmethod
    def add_links_to_queue(cls, links, depth):
        super().add_links_to_queue(links, depth)

    @classmethod
    def update_files(cls):
        super().update_files()


