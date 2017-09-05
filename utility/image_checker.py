from threading import Thread

from rabbitmq.queue_wrapper import QueueWrapper
from utility import responses
from utility.counter import Counter
from utility.logger import Logger
from utility.url_open_wrapper import URLOpenWrapper


class ImageChecker(Thread):
    count = 0

    def __init__(self, mongod):
        Thread.__init__(self)
        self.mongod = mongod
        self.queue = QueueWrapper("image_q")
        self.daemon = True

    def run(self):
        self.queue.start_consuming(self.callback)

    def callback(self, ct, ch, method, properties, body):
        url = body.decode("utf-8")
        Logger.logger.info("Getting Image Status : " + url)
        with URLOpenWrapper(url) as resp:
            if resp.is_successful_response():
                if resp.get_size() == 0:
                    self.mongod.add_image_links_to_missing_images(url, resp.get_status_code(),
                                                                  ('0', "Image is missing"))
            else:
                self.mongod.add_image_links_to_missing_images(url, resp.get_status_code(),
                                                              responses.responses[resp.get_status_code()])
        ch.basic_ack(delivery_tag=method.delivery_tag)
        Counter.total_images += 1
