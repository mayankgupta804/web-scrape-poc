from abc import abstractmethod

from domain_extractor import *
from utilities import *


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

    # Creates directory and files for project on first run and starts the spider
    @classmethod
    def boot(cls):
        create_project_dir(cls.project_name)
        create_data_files(cls.project_name, cls.base_url)
        cls.queue = file_to_set(cls.queue_file)
        cls.crawled = file_to_set(cls.crawled_file)
        cls.spelling = file_to_set(cls.spelling_file)

    # Updates user display, fills queue and updates files
    @classmethod
    def crawl_page(cls, thread_name, page_info):
        if page_info not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_info[0])
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)) + ' | Depth ' + str(
                page_info[1]))
            if int(page_info[1]) < cls.max_depth:
                links = cls.gather_links(page_info[0])
                cls.add_links_to_queue(links, page_info[1])
            Spider.queue.remove(page_info)
            cls.crawled.add(page_info)
            cls.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @abstractmethod
    def gather_links(cls, page_url):
        raise NotImplementedError

    # Saves queue data to project files
    @classmethod
    def add_links_to_queue(cls, links, depth):
        for url in links:
            url = url.rstrip('/')
            if (url in cls.queue) or (url in cls.crawled):
                continue
            if cls.domain_name != get_domain_name(url):
                continue
            cls.queue.add((url, int(depth) + 1))

    @classmethod
    def update_files(cls):
        set_to_file(cls.queue, cls.queue_file)
        set_to_file(cls.crawled, cls.crawled_file)
