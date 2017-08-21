from mongo.constants import Constants


class MongoReader:
    def __init__(self, documents):
        self.documents = documents
        self.urls = self.documents[Constants.CRAWLED_DOCUMENT]
        self.images = self.documents[Constants.MISSING_IMAGES_DOCUMENT]
        self.links = self.documents[Constants.BROKEN_LINKS_DOCUMENT]
        self.spellings = self.documents[Constants.SPELLINGS_DOCUMENT]
        self.blank_page = self.documents[Constants.BLANK_PAGE_DOCUMENT]

    def is_url_crawled(self, url):
        if self.urls.find_one({"url": url}) is None:
            return False
        else:
            return True
