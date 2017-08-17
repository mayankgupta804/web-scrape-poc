from urllib.request import urlopen

from config.property_reader import PropertyReader
from utility.link_finder import LinkFinder
from utility.spell_checker import CheckWords

from utility.image_checker import add_images_to_queue, ImageChecker
from spiders.spider import Spider


class RequestingSpider(Spider):
    image_check = False
    spell_check = False

    def __init__(self, config, base_url, domain_name, mongod):
        Spider.__init__(self, config, base_url, domain_name, mongod)
        Spider.boot(config)
        self.crawl_page('First spider', (Spider.base_url, 0))
        RequestingSpider.image_check = PropertyReader(config).image_check
        RequestingSpider.spell_check = PropertyReader(config).spell_check

        if self.image_check:
            ImageChecker(Spider.broken_images_file).start()
        if self.spell_check:
            CheckWords(Spider.spelling_file).start()

    @classmethod
    def crawl_page(cls, thread_name, page_url):
        super().crawl_page(thread_name, page_url)

    @classmethod
    def gather_links(cls, page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(cls.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
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
