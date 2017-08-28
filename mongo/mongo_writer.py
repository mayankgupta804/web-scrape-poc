from mongo.constants import Constants
from utility.responses import responses


class MongoWriter:
    def __init__(self, documents):
        self.documents = documents
        self.urls = self.documents[Constants.CRAWLED_DOCUMENT]
        self.images = self.documents[Constants.MISSING_IMAGES_DOCUMENT]
        self.broken_links = self.documents[Constants.BROKEN_LINKS_DOCUMENT]
        self.spellings = self.documents[Constants.SPELLINGS_DOCUMENT]
        self.blank_page = self.documents[Constants.BLANK_PAGE_DOCUMENT]

    def write_urls_to_db(self, links, depth):
        posts = []
        for link in links:
            posts.append({"url": link, "depth": depth})

        self.urls.insert_many(posts)

    def write_url_to_db(self, link, depth, status):
        self.urls.insert_one({"url": link.url, "clean_url": link.clean_url, "depth": depth, "response_code": status})

    def add_word_to_dictionary(self, word_dict):
        self.spellings.update({"word": word_dict['word']}, {"word": word_dict['word']}, upsert=True)
        self.spellings.update({"word": word_dict['word']},
                              {'$push': {"info": {"count": word_dict['count'], "url": word_dict['url']}}})

    def add_links_to_blank_page(self, url):
        self.blank_page.insert({"url": url})

    def add_image_links_to_missing_images(self, url, status, status_info):
        self.images.insert({"url": url, "status_code": status, "status": status_info})

    def add_to_broken_links(self, url, status):
        self.broken_links.insert_one({"url": url, "status_code": status, "status": responses[status]})
