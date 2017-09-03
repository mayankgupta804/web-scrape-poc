import threading
from functools import partial

import pika
from pika.exceptions import ConnectionClosed, ChannelClosed

from utility.logger import Logger


class QueueWrapper:
    def __init__(self, queue_name):
        self.queue = queue_name
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1', connection_attempts=5, heartbeat_interval=60))
        self.channel = self._get_channel()

    def _get_channel(self):
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue=self.queue, durable=True)
        return channel

    def start_consuming(self, callback):
        while True:
            try:
                self.channel.basic_consume(partial(callback, threading.currentThread().getName()),
                                           queue=self.queue, consumer_tag=threading.currentThread().getName())
                self.channel.start_consuming()
                break
            except ConnectionClosed as e:
                Logger.logger.error(str(e))
            except ChannelClosed as e:
                Logger.logger.error(str(e))
                self.channel = self._get_channel()
            except Exception as e:
                Logger.logger.info(str(e))
                break
        Logger.logger.info("Exiting Consumer : " + threading.currentThread().getName())

    def push(self, task, header):
        while True:
            try:
                self.channel.basic_publish(exchange='',
                                           routing_key=self.queue,
                                           body=task,
                                           properties=pika.BasicProperties(
                                               delivery_mode=2,  # make message persistent
                                               headers=header
                                           ))
                break
            except ConnectionClosed as e:
                Logger.logger.error(str(e))
                self.channel = self._get_channel()

    def pull(self):
        try:
            return self.channel.basic_get(self.queue)
        except ConnectionClosed as e:
            Logger.logger.error(str(e))
            self.channel = self._get_channel()
            return self.channel.basic_get(self.queue)

    def ack(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    def push_all(self, links, header):
        for link in links:
            if link is not None:
                self.push(link, header)


2
