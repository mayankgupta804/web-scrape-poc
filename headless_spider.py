from driver_init import WebDriverWrapper
from link_finder import LinkFinder
from properties import Properties
from spell_check import CheckWords
from spider import Spider
from utilities import append_to_file


class HeadlessSpider(Spider):
    def __init__(self,config, base_url, domain_name):
        Spider.__init__(self,config, base_url, domain_name)
        Spider.boot(config)
        self.crawl_page('First spider', (Spider.base_url, 0))
        CheckWords(Spider.spelling_file).start()

    @classmethod
    def crawl_page(cls, thread_name, page_url):
        super().crawl_page(thread_name, page_url)

    @classmethod
    def gather_links(cls, page_url):
        try:
            driver = WebDriverWrapper(page_url)
            html_string = driver.get_page_source()
            driver.add_words_to_queue()
            driver.close()
            finder = LinkFinder(cls.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            append_to_file(Properties(cls.config).error_file, str(e))
            return set()
        return finder.page_links()

    @classmethod
    def add_links_to_queue(cls, links, depth):
        super().add_links_to_queue(links, depth)

    @classmethod
    def update_files(cls):
        super().update_files()
