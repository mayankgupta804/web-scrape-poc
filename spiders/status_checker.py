from threading import Thread

from config.properties import Properties
from rabbitmq.queue_wrapper import QueueWrapper
from utility.logger import Logger
from utility.url_open_wrapper import URLOpenWrapper


class StatusCheck(Thread):
    def __init__(self, mongod):
        super().__init__()
        self.mongod = mongod
        self.status_queue = QueueWrapper("status_q")
        self.crawler_queue = QueueWrapper("crawler_q")
        self.daemon = True

    def run(self):
        self.status_queue.start_consuming(self.callback)

    def callback(self, ct, ch, method, properties, body):
        url = body.decode("utf-8")
        if not self.mongod.is_url_crawled(url):
            Logger.logger.info("Getting status : " + url)
            with URLOpenWrapper(url) as page_status:
                headers = properties.headers
                headers['status'] = page_status.get_status_code()
                if page_status.is_successful_response():
                    if headers["depth"] <= Properties.depth:
                        self.crawler_queue.push(url, headers)
                else:
                    self.mongod.add_to_broken_links(url, page_status.get_status_code())
            self.mongod.write_url_to_db(url, headers)
        ch.basic_ack(delivery_tag=method.delivery_tag)