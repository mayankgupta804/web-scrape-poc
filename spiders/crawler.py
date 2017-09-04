from threading import Thread

from config.properties import Properties
from rabbitmq.queue_wrapper import QueueWrapper
from utility.counter import Counter
from utility.driver_wrapper import WebDriverWrapper
from utility.logger import Logger


class Crawler(Thread):
    def __init__(self, mongod):
        super().__init__()
        self.mongod = mongod
        self.crawler_queue = QueueWrapper("crawler_q")
        self.status_queue = QueueWrapper("status_q")
        self.image_queue = QueueWrapper("image_q")
        self.daemon = True

    def run(self):
        self.crawler_queue.start_consuming(self.callback)

    def callback(self, ct, ch, method, properties, body):
        url = body.decode("utf-8")
        Logger.logger.info(self.getName() + " processing " + url)
        self.crawl(url, properties.headers)
        Counter.url += 1
        Logger.logger.info(self.getName() + " finished processing " + url)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # ch.basic_cancel(ct)

    def crawl(self, url, header):
        try:
            with WebDriverWrapper(url, Properties.device, self.mongod) as driver:
                links = driver.get_all_links()
                img_links = driver.get_image_links()
                driver.is_blank_page()
                driver.add_words_to_queue()
        except Exception as e:
            Logger.logger.error(str(e))
            return
        self.mongod.update_url_to_crawled(url)
        self.status_queue.push_all(links, {"depth": header["depth"] + 1,
                                           "parent": url})
        self.image_queue.push_all(img_links, {"parent": url})
