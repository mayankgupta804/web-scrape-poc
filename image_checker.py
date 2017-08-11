from multiprocessing import JoinableQueue
from threading import Thread
from urllib.request import urlopen

from spider import Spider
from url_open_wrapper import URLOpenWrapper

q = JoinableQueue(1000)

def add_images_to_queue(links):
    q.put(links)

class ImageChecker(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self._file = file_name

    def run(self):
        while True:
            link = q.get()
            status = URLOpenWrapper(link).get_status_code()
            if int(status) == 200:
                if self.get_image_size(link) <= 0:
                    cls.broken_images.add(str(status), Spider.request[status],link)
            elif int(status) != 200:
                cls.broken_images.add((str(status), Spider.request[status], page_info[0]))

    def get_image_size(self,page_url):
        file = urlopen(page_url)
        return len(file.read())