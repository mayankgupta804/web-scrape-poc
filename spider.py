from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
from driver import *
from spell_check import *


class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    spelling_file = ''
    max_depth = int()
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name, max_depth):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.max_depth = max_depth
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.spelling_file = Spider.project_name + '/spelling.txt'
        self.boot()
        self.crawl_page('First spider', (Spider.base_url, 0))
        CheckWords(Spider.spelling_file).start()

    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)
        Spider.spelling = file_to_set(Spider.spelling_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_info):
        if page_info not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_info[0])
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)) + ' | Depth ' + str(page_info[1]))
            if int(page_info[1]) < Spider.max_depth:
                Spider.add_links_to_queue(Spider.gather_links(page_info[0]), page_info[1])
            Spider.queue = set(filter(lambda x: x[0] != page_info[0], Spider.queue))
            Spider.crawled.add(page_info)
            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        try:
            driver = WebDriverWrapper(page_url)
            driver.save_screenshot()
            html_string = driver.get_page_source()
            driver.add_words_to_queue()
            driver.close()
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links, depth):
        for url in links:
            url = url.rstrip('/')
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add((url, int(depth) + 1))

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
