from threading import Thread

import pika

from rabbitmq.connect import get_rabbit_mq_channel
from spiders.headless_spider import HeadlessSpider
from spiders.spider import Spider


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
        HeadlessSpider.crawl_page(self.getName(), body.decode("utf-8"), properties.headers['depth'], self._channel)
        ch.basic_ack(delivery_tag=method.delivery_tag)

