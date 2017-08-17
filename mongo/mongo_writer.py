class MongoWriter:
    def __init__(self, db):
        self.db = db
        self.urls = self.db["urls"]
        self.images = self.db["images"]
        self.links = self.db["links"]
        self.spellings = self.db["spellings"]
        self.blank_page = self.db["blankpage"]

    def write_urls_to_db(self, links, depth):
        posts = []
        for link in links:
            posts.append({"url": link, "depth": depth})

        self.urls.insert_many(posts)

    def add_word_to_dictionary(self, dict):
        self.spellings.update({"word": dict['word']}, {"word": dict['word']}, upsert=True)
        self.spellings.update({"word": dict['word']},
                              {'$push': {"info": {"count": dict['count'], "url": dict['url']}}})

    def add_links_to_blank_page(self, url):
        self.blank_page.insert({"url": url})

    def add_image_links_to_missing_images(self, url, status, status_info):
        self.images.insert({"url": url, "status": status, "status_info": status_info})
