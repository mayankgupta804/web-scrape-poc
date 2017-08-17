class MongoReader:
    def __init__(self, db):
        self.db = db
        self.urls = self.db["urls"]
        self.images = self.db["images"]
        self.links = self.db["links"]
        self.spellings = self.db["spellings"]
