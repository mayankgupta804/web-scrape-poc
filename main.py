import threading
from multiprocessing import JoinableQueue

from headless_spider import HeadlessSpider
from requesting_spider import RequestingSpider
from spider import Spider
from domain_extractor import *
from utilities import *

FOLDER_NAME = 'test'
HOMEPAGE = 'http://www.testvagrant.com'
NUMBER_OF_THREADS = 20
MODE = input("Select mode (light|heavy) : ")
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = FOLDER_NAME + '/queue.txt'
CRAWLED_FILE = FOLDER_NAME + '/crawled.txt'
queue = JoinableQueue()
if MODE == 'heavy':
    spider = HeadlessSpider(FOLDER_NAME, HOMEPAGE, DOMAIN_NAME)
elif MODE == 'light':
    spider = RequestingSpider(FOLDER_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range (NUMBER_OF_THREADS):
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
