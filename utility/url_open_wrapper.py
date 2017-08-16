import nltk
import requests

from utility.spell_checker import *


class URLOpenWrapper:
    def __init__(self, page_url):
        self._page_url = page_url
        self._response = requests.get(page_url)

    def get_page_source(self):
        if 'text/html' in self._response.headers('Content-Type'):
            html_bytes = self._response.raw()
            return html_bytes.decode("utf-8")
        else:
            return None

    def add_words_to_queue(self):
        add_words_to_queue(nltk.clean_html(self._response), self._page_url)

    def get_status_code(self):
        return self._response.status_code
