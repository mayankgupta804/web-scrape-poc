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

    def get_crawled_urls_count(self):
        return self.urls.count()

    def get_missing_images_count(self):
        return self.images.count()

    def get_broken_links_count(self):
        return self.links.count()

    def get_spellings_count(self):
        return self.spellings.count()

    def get_blank_page_count(self):
        return self.blank_page.count()
