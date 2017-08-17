class MongoWriter:
    def __init__(self, db):
        self.db = db
        self.urls = self.db["urls"]
        self.images = self.db["images"]
        self.links = self.db["links"]
        self.spellings = self.db["spellings"]

    def write_urls_to_db(self, links, depth):
        posts = []
        for link in links:
            posts.append({"url": link, "depth": depth})

        self.urls.insert_many(posts)
