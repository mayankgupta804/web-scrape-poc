import time

from pymongo import MongoClient

from mongo.mongo_reader import MongoReader
from mongo.mongo_writer import MongoWriter


class MongoDB(MongoReader, MongoWriter):
    def __init__(self, *args):
        if len(args) == 0:
            self.client = MongoClient()
        else:
            self.client = MongoClient(args)

        self.db = self.client["Crawler" + str(int(time.time()))]
        super().__init__(self.db)
