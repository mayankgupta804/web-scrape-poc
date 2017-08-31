from threading import Thread

from multiprocessing import JoinableQueue

import pika
from pika.exceptions import ConnectionClosed

from config.properties import Properties
from rabbitmq.connect import get_rabbit_mq_channel
from utility.domain_extractor import get_domain_name
from utility.logger import Logger
from utility.url import Url

q = JoinableQueue()


def add_links_to_queue(links, depth, thread_name, parent_url, domain_name):
    Logger.logger.info(thread_name + " adding " + str(len(links)) + " links to queue.")
    for link in links:
        url = Url(link)
        if domain_name != get_domain_name(str(url)):
            continue
        if depth < Properties.depth:
            q.put((str(url), depth + 1, parent_url))


class WriterQueue(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        try:
            channel = get_rabbit_mq_channel()
            # channel.basic_qos(prefetch_count=1)
            while True:
                data = q.get()
                while True:
                    try:
                        channel.basic_publish(exchange='',
                                              routing_key='links_queue',
                                              body=data[0],
                                              properties=pika.BasicProperties(
                                                  delivery_mode=2,  # make message persistent
                                                  headers={'depth': data[1],
                                                           'parent': data[2]
                                                           }
                                              ))
                        break
                    except ConnectionClosed as e:
                        Logger.logger.error(str(e))
                        channel = get_rabbit_mq_channel()

        except EOFError as e:
            Logger.logger.info("Spell checker EOFError : " + str(e))
