from config.properties import Properties
from mongo.mongodb import MongoDB
from rabbitmq.queue_wrapper import QueueWrapper
from report.excel_report_generator import ExcelReport
from spiders.crawler import Crawler
from spiders.status_checker import StatusCheck
from utility.domain_extractor import get_domain_name
from utility.logger import Logger

Logger.logger.info("starting...")
HOMEPAGE = Properties.home_page
DOMAIN_NAME = get_domain_name(HOMEPAGE)
threads = []
mongod = MongoDB()

QueueWrapper("status_q").push(Properties.home_page, {'depth': 0,
                                                     'parent': "root"
                                                     })
StatusCheck(mongod).start()


# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(Properties.threads):
        thrd = Crawler(mongod)
        thrd.start()
        threads.append(thrd)
        Logger.logger.info("Thread %r started", thrd.getName())


create_workers()

for thread in threads:
    thread.join()

ExcelReport(mongod).create_workbook()
