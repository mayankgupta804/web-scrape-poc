import time
from threading import Thread

from pika.exceptions import ConnectionClosed

from rabbitmq.connect import get_rabbit_mq_channel
from spiders.headless_spider import HeadlessSpider
from utility.counter import Counter
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
            method_frame, header_frame, body = self.get_task()
            if method_frame:
                counter = 0
                url = Url(body.decode("utf-8"))
                Logger.logger.info(self.getName() + " processing " + str(url))
                success = HeadlessSpider.crawl_page(self.getName(), url, header_frame.headers['depth'], self._channel)
                if success:
                    self._channel.basic_ack(method_frame.delivery_tag)
                Counter.url += 1
                Logger.logger.info(self.getName() + " finished processing " + str(url))
            else:
                time.sleep(10)
                counter += 1
        Logger.logger.info("exiting thread : " + self.getName())

    def get_task(self):
        try:
            return self._channel.basic_get('links_queue')
        except ConnectionClosed as e:
            Logger.logger.error(str(e))
            self._channel = get_rabbit_mq_channel()
            self._channel.basic_qos(prefetch_count=1)
            return self._channel.basic_get('links_queue')
