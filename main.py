import sys
import threading
from multiprocessing import JoinableQueue

import time

from domain_extractor import *
from headless_spider import HeadlessSpider
from requesting_spider import RequestingSpider
from utilities import *

if len(sys.argv) > 1:
    CONFIG = sys.argv[1]
else:
    CONFIG = "config.properties"

p = PropertiesHelper(CONFIG)

FOLDER_NAME = p.folder
HOMEPAGE = p.home_page
NUMBER_OF_THREADS = p.threads
MODE = p.mode
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = p.queue_file
CRAWLED_FILE = p.crawled_file
SPELLINGS_FILE = p.spelling_file
BROKEN_LINKS = p.broken_links_file
MAX_DEPTH = p.depth
BROKEN_IMAGES = p.broken_images_file
queue = JoinableQueue()
sys.setrecursionlimit(10000)

if MODE == 'normal':
    spider = HeadlessSpider(CONFIG, HOMEPAGE, DOMAIN_NAME)
elif MODE == 'light':
    spider = RequestingSpider(CONFIG, HOMEPAGE, DOMAIN_NAME)

start = time.time()

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
print('Elapsed time : %s',(time.time()-start))
