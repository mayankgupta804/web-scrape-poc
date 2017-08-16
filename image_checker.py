from multiprocessing import JoinableQueue
from threading import Thread
from urllib.request import urlopen

from url_open_wrapper import URLOpenWrapper
from utilities import append_to_file, set_to_file

queue = JoinableQueue(1000)

def add_images_to_queue(links):
    for link in links:
        queue.put(link)

def get_image_size(page_url):
    file = urlopen(page_url)
    return len(file.read())

class ImageChecker(Thread):

    request = {
        301: 'Moved Permanently',
        302: 'Redirect',
        400: 'Bad Request',
        401: 'Unauthorised',
        403: 'Forbidden',
        404: 'Not Found',
        408: 'Request Timeout',
        500: 'Internal Server Error'
    }

    def __init__(self, file_name):
        Thread.__init__(self)
        self._file = file_name
        self.daemon = True

    def run(self):

        while True:
            link = queue.get()
            status = URLOpenWrapper(link).get_status_code()
            if int(status) == 200:
                if get_image_size(link) == 0:
                   append_to_file(self._file,str(status) + "," + ImageChecker.request[status] + "," + link)
            elif int(status) != 200:
               append_to_file(self._file, str(status) + "," + ImageChecker.request[status] + "," + link)
            queue.task_done()
