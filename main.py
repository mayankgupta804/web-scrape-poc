from config.properties import Properties
from mongo.mongodb import MongoDB
from rabbitmq.queue_wrapper import QueueWrapper
from report.excel_report_generator import ExcelReport
from spiders.crawler import Crawler
from spiders.status_checker import StatusCheck
from utility.logger import Logger

Logger.logger.info("starting...")
threads = []
mongod = MongoDB()

QueueWrapper("status_q").push(Properties.home_page, {'depth': 0,
                                                     'parent': "root"
                                                     })

for _ in range(Properties.threads):
    thrd1, thrd2 = Crawler(mongod), StatusCheck(mongod)
    thrd1.start()
    thrd2.start()
    threads.append(thrd1)
    threads.append(thrd2)
    Logger.logger.info("Crawler Thread %r started", thrd1.getName())
    Logger.logger.info("Status Check Thread %r started", thrd2.getName())

try:
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    ExcelReport(mongod).create_workbook()
