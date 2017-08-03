from abc import abstractmethod
from domain_extractor import *
from utilities import *

class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()


    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

    # Creates directory and files for project on first run and starts the spider
    @classmethod
    def boot(cls):
        create_project_dir(cls.project_name)
        create_data_files(cls.project_name, cls.base_url)
        cls.queue = file_to_set(cls.queue_file)
        cls.crawled = file_to_set(cls.crawled_file)

    # Updates user display, fills queue and updates files
    @classmethod
    def crawl_page(cls,thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(cls.queue)) + ' | Crawled  ' + str(len(cls.crawled)))
            cls.add_links_to_queue(cls.gather_links(page_url))
            cls.queue.remove(page_url)
            cls.crawled.add(page_url)
            cls.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @abstractmethod
    def gather_links(cls,page_url):
        raise NotImplementedError

    # Saves queue data to project files
    @classmethod
    def add_links_to_queue(cls,links):
        for url in links:
            if (url in cls.queue) or (url in cls.crawled):
                continue
            if cls.domain_name != get_domain_name(url):
                continue
            cls.queue.add(url)

    @classmethod
    def update_files(cls):
        set_to_file(cls.queue, cls.queue_file)
        set_to_file(cls.crawled, cls.crawled_file)
