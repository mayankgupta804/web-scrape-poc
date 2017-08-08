import threading
from multiprocessing import JoinableQueue

import sys

from headless_spider import HeadlessSpider
from properties import Properties
from requesting_spider import RequestingSpider
from domain_extractor import *
from utilities import *

if len(sys.argv) > 1:
    p = Properties(sys.argv[1])
else:
    p = Properties()
FOLDER_NAME = p.folder
HOMEPAGE = p.home_page
NUMBER_OF_THREADS = p.threads
MODE = p.mode
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = p.queue_file
CRAWLED_FILE = p.crawled_file
SPELLINGS_FILE = p.spelling_file
FAILED_URLs = p.failed_file
MAX_DEPTH = p.depth
queue = JoinableQueue()
sys.setrecursionlimit(10000)

if MODE == 'normal':
    spider = HeadlessSpider(FOLDER_NAME, HOMEPAGE, DOMAIN_NAME, MAX_DEPTH)
elif MODE == 'light':
    spider = RequestingSpider(FOLDER_NAME, HOMEPAGE, DOMAIN_NAME, MAX_DEPTH)


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


create_workers()
crawl()
