from multiprocessing import JoinableQueue
from threading import Thread
from urllib.request import urlopen

from spiders.spider import Spider
from utility.utilities import append_to_file

from utility.url_open_wrapper import URLOpenWrapper

queue = JoinableQueue(1000)


def add_images_to_queue(links):
    for link in links:
        queue.put(link)


def get_image_size(page_url):
    file = urlopen(page_url)
    return len(file.read())


class ImageChecker(Thread):
    count = 0

    def __init__(self, mongod):
        Thread.__init__(self)
        self.mongod = mongod
        self.daemon = True
        ImageChecker.count = 0

    def run(self):

        while True:
            link = queue.get()
            status = URLOpenWrapper(link).get_status_code()
            if int(status) == 200:
                if get_image_size(link) == 0:
                    self.mongod.add_image_links_to_missing_images(link, status, Spider.request[status])
                    ImageChecker.count += 1
            elif int(status) != 200:
                self.mongod.add_image_links_to_missing_images(link, status, Spider.request[status])
                ImageChecker.count += 1
            if ImageChecker.count > 0:
                print('Broken Images : ', ImageChecker.count)
            else:
                pass
            queue.task_done()
