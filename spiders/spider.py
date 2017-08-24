from abc import abstractmethod

import pika

from config.properties import Properties
from utility.domain_extractor import *
from utility.logger import Logger
from utility.responses import responses
from utility.url import Url
from utility.url_open_wrapper import URLOpenWrapper


class Spider:
    mongod = None
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    broken_links_file = ''
    spelling_file = ''
    broken_images_file = ''
    blank_pages_file = ''
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

    def __init__(self, base_url, domain_name, mongod):
        Spider.mongod = mongod
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.max_depth = Properties.depth

    # Updates user display, fills queue and updates files
    @classmethod
    def crawl_page(cls, thread_name, page_url, depth, channel):
        if not cls.mongod.is_url_crawled(page_url.clean_url):
            with URLOpenWrapper(page_url.clean_url) as page_status:
                if page_status.is_successful_response():
                    print(thread_name + ' now crawling ' + page_url.url)
                    if depth <= cls.max_depth:
                        cls.add_links_to_queue(cls.gather_links(page_url.url), depth, channel, thread_name)
                else:
                    cls.mongod.add_to_broken_links(page_url.url, page_status.get_status_code())
                cls.mongod.write_url_to_db(page_url, depth, page_status.get_status_code())

    # Converts raw response data into readable information and checks for proper html formatting
    @abstractmethod
    def gather_links(self, page_url):
        raise NotImplementedError

    # Saves queue data to project files
    @classmethod
    def add_links_to_queue(cls, links, depth, channel, thread_name):
        Logger.logger.info(thread_name + " adding " + str(len(links)) + " links to queue.")
        for link in links:
            url = Url(link)
            if cls.domain_name != get_domain_name(str(url)):
                continue
            if depth < cls.max_depth:
                channel.basic_publish(exchange='',
                                      routing_key='task_queue',
                                      body=str(url),
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,  # make message persistent
                                          headers={'depth': depth + 1}
                                      ))
