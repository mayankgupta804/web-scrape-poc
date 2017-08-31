from config.properties import Properties
from mongo.mongodb import MongoDB
from report.excel_report_generator import ExcelReport
from spiders.crawler import Crawler
from spiders.headless_spider import HeadlessSpider
from spiders.requesting_spider import RequestingSpider
from utility.domain_extractor import get_domain_name
from utility.logger import Logger


Logger.logger.info("starting...")
HOMEPAGE = Properties.home_page
MODE = Properties.mode
DOMAIN_NAME = get_domain_name(HOMEPAGE)
threads = []
mongod = MongoDB()

if MODE == 'normal':
    spider = HeadlessSpider(HOMEPAGE, DOMAIN_NAME, mongod)
elif MODE == 'light':
    spider = RequestingSpider(HOMEPAGE, DOMAIN_NAME, mongod)


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

ExcelReport(mongod).create_workbook()
# Report(mongod).create_header_table()
