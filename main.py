import sys
import threading
from multiprocessing import JoinableQueue

import time

from mongo.mongodb import MongoDB
from spiders.requesting_spider import RequestingSpider
from utility.utilities import *

from utility.domain_extractor import *
from spiders.headless_spider import HeadlessSpider

# if len(sys.argv) > 1:
#     CONFIG = sys.argv[1]
# else:
#     CONFIG = "config.properties"


FOLDER_NAME = Properties.folder
HOMEPAGE = Properties.home_page
NUMBER_OF_THREADS = Properties.threads
MODE = Properties.mode
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = Properties.queue_file
queue = JoinableQueue()
sys.setrecursionlimit(10000)

if MODE == 'normal':
    spider = HeadlessSpider(HOMEPAGE, DOMAIN_NAME, MongoDB())
elif MODE == 'light':
    spider = RequestingSpider(HOMEPAGE, DOMAIN_NAME, MongoDB())

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()
    else:
        sys.exit(0)


create_workers()
crawl()
