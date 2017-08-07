from urllib.request import urlopen

from link_finder import LinkFinder
from spell_check import CheckWords
from spider import Spider


class RequestingSpider(Spider):

    def __init__(self, project_name, base_url, domain_name,max_depth):
        Spider.__init__(self, project_name, base_url, domain_name,max_depth)
        Spider.boot()
        self.crawl_page('First spider', Spider.base_url)
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
        return finder.page_links()

    @classmethod
    def add_links_to_queue(cls, links,depth):
        super().add_links_to_queue(links,depth)

    @classmethod
    def update_files(cls):
        super().update_files()
