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

    def add_word_to_dictionary(self, dict):
        self.spellings.update({"word": dict['word']},{"word": dict['word']}, upsert=True)
        self.spellings.update({"word": dict['word']},
                              {'$push': {"info": {"count": dict['count'], "url": dict['url']}}})
