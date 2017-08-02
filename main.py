import threading
from multiprocessing import JoinableQueue
from spider import Spider
from domain import *
from general import *

FOLDER_NAME = input("Enter the project name : ")
HOMEPAGE = input("Enter URL of the homepage : ")
STR_NUMBER_OF_THREADS = input("Enter number of threads for crawling : ")
NUMBER_OF_THREADS = int(STR_NUMBER_OF_THREADS)
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = FOLDER_NAME + '/queue.txt'
CRAWLED_FILE = FOLDER_NAME + '/crawled.txt'
SPELLINGS_FILE = FOLDER_NAME + 'spellings.txt'
queue = JoinableQueue()
Spider(FOLDER_NAME, HOMEPAGE, DOMAIN_NAME)


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
        Spider.crawl_page(threading.current_thread().name, url)
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
