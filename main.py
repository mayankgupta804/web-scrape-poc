import sys
from multiprocessing import JoinableQueue

from config.properties import Properties
from mongo.mongodb import MongoDB
from spiders.crawler import Crawler
from spiders.headless_spider import HeadlessSpider
from spiders.requesting_spider import RequestingSpider
from utility.domain_extractor import *

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
        Crawler().start()


create_workers()
