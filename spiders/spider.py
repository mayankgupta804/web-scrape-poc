from abc import abstractmethod
from utility.domain_extractor import *
from utility.utilities import *

from utility.url_open_wrapper import URLOpenWrapper

class Spider:
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    broken_links_file = ''
    spelling_file = ''
    broken_images_file = ''
    max_depth = int()
    queue = set()
    crawled = set()
    broken_links = set()
    request = {
        301: 'Moved Permanently',
        302: 'Redirect',
        400: 'Bad Request',
        401: 'Unauthorised',
        403: 'Forbidden',
        404: 'Not Found',
        408: 'Request Timeout',
        500: 'Internal Server Error'
    }

    def __init__(self, config, base_url, domain_name):
        p = Properties(config)
        self.config = config
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.max_depth = p.depth
        Spider.queue_file = p.queue_file
        Spider.crawled_file = p.crawled_file
        Spider.spelling_file = p.spelling_file
        Spider.broken_links_file = p.broken_links_file
        Spider.broken_images_file = p.broken_images_file

    # Creates directory and files for project on first run and starts the spider
    @classmethod
    def boot(cls, config):
        create_data_files(config)
        cls.queue = file_to_set(cls.queue_file)
        cls.crawled = file_to_set(cls.crawled_file)
        cls.spelling = file_to_set(cls.spelling_file)

    # Updates user display, fills queue and updates files
    @classmethod
    def crawl_page(cls, thread_name, page_info):
        if page_info[0] not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_info[0])
            print('Queue : ' + str(len(Spider.queue)) + ' | Crawled : ' + str(len(Spider.crawled)) + ' | Depth : ' + str(
                page_info[1]) + ' | Broken Links : ' + str(len(Spider.broken_links)))
            cls.add_links_per_depth(page_info)
            Spider.queue.remove(page_info)
            cls.crawled.add(page_info)
            cls.check_link_status(page_info)
            cls.update_files()

    @classmethod
    def add_links_per_depth(cls, page_info):
        if int(page_info[1]) <= cls.max_depth:
            links = cls.gather_links(page_info[0])
            cls.add_links_to_queue(links, page_info[1])

    @classmethod
    def check_link_status(cls, page_info):
        status = URLOpenWrapper(page_info[0]).get_status_code()
        if status in Spider.request:
            cls.broken_links.add((str(status), Spider.request[status], page_info[0]))

    # Converts raw response data into readable information and checks for proper html formatting
    @abstractmethod
    def gather_links(cls, page_url):
        raise NotImplementedError


    # Saves queue data to project files
    @classmethod
    def add_links_to_queue(cls, links, depth):
        for url in links:
            url = url.rstrip('/')
            if ((url,depth) in cls.queue) or ((url,depth) in cls.crawled):
                continue
            if cls.domain_name != get_domain_name(url):
                continue
            if depth < cls.max_depth:
                cls.queue.add((url, int(depth) + 1))

    @classmethod
    def update_files(cls):
        set_to_file(cls.queue, cls.queue_file)
        set_to_file(cls.crawled, cls.crawled_file)
        set_to_file(cls.broken_links, cls.broken_links_file)
