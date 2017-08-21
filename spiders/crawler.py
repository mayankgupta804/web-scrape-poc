from threading import Thread

import pika

from rabbitmq.connect import get_rabbit_mq_channel
from spiders.headless_spider import HeadlessSpider
from spiders.spider import Spider
from utility.logger import Logger


class Crawler(Thread):
    def __init__(self):
        super().__init__()
        self._channel = self.create_connection()
        self.daemon = True

    # @staticmethod
    def create_connection(self):
        channel = get_rabbit_mq_channel()

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.crawl,
                              queue='task_queue')
        return channel

    def run(self):
        self._channel.start_consuming()

    def crawl(self, ch, method, properties, body):
        url = body.decode("utf-8")
        Logger.logger.info(self.getName() + " processing " + url)
        HeadlessSpider.crawl_page(self.getName(), url, properties.headers['depth'], self._channel)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        Logger.logger.info(self.getName() + " finished processing " + url)
