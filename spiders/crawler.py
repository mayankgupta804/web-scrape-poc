import time
from threading import Thread

from rabbitmq.connect import get_rabbit_mq_channel
from spiders.headless_spider import HeadlessSpider
from utility.logger import Logger
from utility.url import Url


class Crawler(Thread):
    def __init__(self):
        super().__init__()
        self._channel = self.create_connection()
        self.daemon = True

    @staticmethod
    def create_connection():
        channel = get_rabbit_mq_channel()
        channel.basic_qos(prefetch_count=1)
        return channel

    def run(self):
        counter = 0
        while counter < 3:
            method_frame, header_frame, body = self._channel.basic_get('task_queue')
            if method_frame:
                counter = 0
                url = Url(body.decode("utf-8"))
                Logger.logger.info(self.getName() + " processing " + str(url))
                HeadlessSpider.crawl_page(self.getName(), url, header_frame.headers['depth'], self._channel)
                self._channel.basic_ack(method_frame.delivery_tag)
                Logger.logger.info(self.getName() + " finished processing " + str(url))
            else:
                time.sleep(10)
                counter += 1
        Logger.logger.info("exiting thread : " + self.getName())
