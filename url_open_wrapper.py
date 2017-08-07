from urllib.request import urlopen
from spell_check import *
import nltk


class URLOpenWrapper:
    def __init__(self,page_url):
        self._page_url = page_url
        self._response = urlopen(page_url)

    def get_page_source(self):
        if 'text/html' in self._response.getheader('Content-Type'):
            html_bytes = self._response.read()
            return html_bytes.decode("utf-8")
        else:
            return None

    def add_words_to_queue(self):
        add_words_to_queue(nltk.clean_html(self._response), self._page_url)

    def get_status_code(self):
        return self._response.getcode()

