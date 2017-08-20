from pymongo import MongoClient
import time

from mongo.mongo_query import MongoQuery
from mongo.mongo_reader import MongoReader
from mongo.mongo_writer import MongoWriter


class MongoDB(MongoReader, MongoWriter, MongoQuery):
    def __init__(self, *args):
        if len(args) == 0:
            self.client = MongoClient()
        else:
            self.client = MongoClient(args)

        self.db = self.client[str(int(time.time()))]
        super().__init__(self.db)

