class MongoQuery:
    def __init__(self, db):
        self.db = db
        self.urls = self.db["urls"]
        self.images = self.db["images"]
        self.links = self.db["links"]
        self.spellings = self.db["spellings"]
        self.blank_page = self.db["blankpage"]

    def is_url_crawled(self, url):
        if self.urls.find_one({"url": url}) is None:
            return False
        else:
            return True
