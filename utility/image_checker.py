from multiprocessing import JoinableQueue
from threading import Thread

from utility import responses
from utility.counter import Counter
from utility.logger import Logger
from utility.url_open_wrapper import URLOpenWrapper

queue = JoinableQueue()


def add_images_to_queue(links):
    for link in links:
        queue.put(link)


class ImageChecker(Thread):
    count = 0

    def __init__(self, mongod):
        Thread.__init__(self)
        self.mongod = mongod
        self.daemon = True

    def run(self):

        try:
            while True:
                link = queue.get()
                with URLOpenWrapper(link) as resp:
                    if resp.is_successful_response():
                        if resp.get_size() == 0:
                            self.mongod.add_image_links_to_missing_images(link, resp.get_status_code(),
                                                                          ('0', "Image is missing"))
                    else:
                        try:
                            self.mongod.add_image_links_to_missing_images(link, resp.get_status_code(),
                                                                          responses.responses[resp.get_status_code()])
                        except KeyError as e:
                            Logger.logger.error("Key error : " + link)
                            Logger.logger.error(str(e))
                queue.task_done()
                Counter.total_images += 1
        except EOFError as e:
            Logger.logger.error("Image checker EOFError : " + str(e))
