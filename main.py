import sys

from config.properties import Properties
from mongo.mongodb import MongoDB
from spiders.crawler import Crawler
from spiders.headless_spider import HeadlessSpider
from spiders.requesting_spider import RequestingSpider
from utility.domain_extractor import get_domain_name
from utility.logger import Logger

HOMEPAGE = Properties.home_page
MODE = Properties.mode
DOMAIN_NAME = get_domain_name(HOMEPAGE)
threads = []

if MODE == 'normal':
    spider = HeadlessSpider(HOMEPAGE, DOMAIN_NAME, MongoDB())
elif MODE == 'light':
    spider = RequestingSpider(HOMEPAGE, DOMAIN_NAME, MongoDB())


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(Properties.threads):
        thrd = Crawler()
        thrd.start()
        threads.append(thrd)
        Logger.logger.info("Thread %r started", thrd.getName())


create_workers()

for thread in threads:
    thread.join()
