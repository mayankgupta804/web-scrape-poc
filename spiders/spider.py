from abc import abstractmethod

import pika

from config.properties import Properties
from rabbitmq.connect import get_rabbit_mq_channel
from utility.domain_extractor import *
from utility.logger import Logger
from utility.utilities import *

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
        if not cls.mongod.is_url_crawled(page_url):
            print(thread_name + ' now crawling ' + page_url)
            print('Queue : ' + str(len(Spider.queue)) + ' | Crawled : ' + str(len(Spider.crawled)) +
                  ' | Depth : ' + str(depth) + ' | Broken Links : ' + str(len(Spider.broken_links)))
            if depth <= cls.max_depth:
                cls.add_links_to_queue(cls.gather_links(page_url), depth, channel, thread_name)
            status = cls.check_link_status(page_url)
            cls.mongod.write_url_to_db(page_url, depth, status)

    @classmethod
    def check_link_status(cls, page_info):
        status = URLOpenWrapper(page_info).get_status_code()
        if status in Spider.request:
            cls.broken_links.add((str(status), Spider.request[status], page_info))
        return status

    # Converts raw response data into readable information and checks for proper html formatting
    @abstractmethod
    def gather_links(self, page_url):
        raise NotImplementedError

    # Saves queue data to project files
    @classmethod
    def add_links_to_queue(cls, links, depth, channel, thread_name):
        Logger.logger.info(thread_name + " adding " + str(len(links)) + " links to queue.")
        for url in links:
            url = url.rstrip('/')
            if cls.domain_name != get_domain_name(url):
                continue
            if depth < cls.max_depth:
                channel.basic_publish(exchange='',
                                      routing_key='task_queue',
                                      body=url,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2,  # make message persistent
                                          headers={'depth': depth + 1}
                                      ))
