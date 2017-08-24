from multiprocessing import JoinableQueue
from threading import Thread

from utility import responses
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
        ImageChecker.count = 0

    def run(self):

        try:
            while True:
                link = queue.get()
                with URLOpenWrapper(link) as resp:
                    if resp.is_successful_response():
                        if resp.get_size() == 0:
                            self.mongod.add_image_links_to_missing_images(link, resp.get_status_code(),
                                                                          "Image is missing")
                            ImageChecker.count += 1
                    else:
                        self.mongod.add_image_links_to_missing_images(link, resp.get_status_code(),
                                                                      responses.responses[resp.get_status_code()])
                        ImageChecker.count += 1
                    if ImageChecker.count > 0:
                        print('Broken Images : ', ImageChecker.count)
                queue.task_done()
        except EOFError as e:
            Logger.logger.info("Image checker EOFError : " + str(e))
