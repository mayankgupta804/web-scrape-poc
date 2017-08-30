from mongo.constants import Constants


class MongoReader:
    def __init__(self, documents):
        self.documents = documents
        self.urls = self.documents[Constants.CRAWLED_DOCUMENT]
        self.images = self.documents[Constants.MISSING_IMAGES_DOCUMENT]
        self.broken_links = self.documents[Constants.BROKEN_LINKS_DOCUMENT]
        self.spellings = self.documents[Constants.SPELLINGS_DOCUMENT]
        self.blank_page = self.documents[Constants.BLANK_PAGE_DOCUMENT]

    def is_url_crawled(self, url):
        if self.urls.find_one({"clean_url": url}) is None:
            return False
        else:
            return True

    def get_crawled_urls_count(self):
        return self.urls.count()

    def get_missing_images_count(self):
        return self.images.count()

    def get_broken_links_count(self):
        return self.broken_links.count()

    def get_spellings_count(self):
        return self.spellings.count()

    def get_blank_page_count(self):
        return self.blank_page.count()

    def get_all_spellings(self):
        data = []
        spellings = list(self.spellings.find())
        for spelling in spellings:
            word = spelling["word"]
            for i, item in enumerate(spelling["info"]):
                if i is 0:
                    data.append([word, str(item["count"]), item["url"]])
                else:
                    data.append(["", str(item["count"]), item["url"]])
        return data

    def get_all_broken_links(self):
        data = []
        broken_links = list(self.broken_links.find())
        for link in broken_links:
            data.append([link['url'], str(link['status_code']), ','.join(link['status'])])
        return data

    def get_all_missing_images(self):
        data = []
        missing_images = list(self.images.find())
        for link in missing_images:
            data.append([link['url'], str(link['status_code']), ','.join(link['status'])])
        return data
