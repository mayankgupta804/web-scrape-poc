import ssl
import urllib.request
from urllib.error import HTTPError, URLError

import nltk

from utility.spell_checker import *


class URLOpenWrapper:
    def __init__(self, page_url):
        self._page_url = page_url
        try:
            gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self._response = urllib.request.urlopen(page_url, context=gcontext)
            self._response_code = self._response.getcode()
        except HTTPError as e:
            Logger.logger.error('The server couldn\'t fulfill the request.')
            Logger.logger.error('Error code: ' + str(e.code))
            self._response_code = e.code
        except URLError as e:
            Logger.logger.error('We failed to reach a server.')
            Logger.logger.error('Reason: ' + str(e.reason))
            self._response_code = 0
        except ValueError as e:
            Logger.logger.error("Value error : " + self._page_url)
            Logger.logger.error("Reason : " + str(e))

    def get_page_source(self):
        if 'text/html' in self._response.headers('Content-Type'):
            html_bytes = self._response.raw()
            return html_bytes.decode("utf-8")
        else:
            return None

    def add_words_to_queue(self):
        add_words_to_queue(nltk.clean_html(self._response), self._page_url)

    def get_status_code(self):
        return self._response_code

    def get_size(self):
        return len(self._response.read())
