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
                resp = URLOpenWrapper(link)
                status = resp.get_status_code()
                if resp.is_successful_response():
                    if resp.get_size() == 0:
                        self.mongod.add_image_links_to_missing_images(link, status, "Image is missing")
                        ImageChecker.count += 1
                else:
                    self.mongod.add_image_links_to_missing_images(link, status, responses.responses[status])
                    ImageChecker.count += 1
                if ImageChecker.count > 0:
                    print('Broken Images : ', ImageChecker.count)
                queue.task_done()
        except EOFError as e:
            Logger.logger.info("Image checker EOFError : " + str(e))


