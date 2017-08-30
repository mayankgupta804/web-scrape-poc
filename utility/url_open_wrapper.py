import ssl
import urllib.request
from _ssl import SSLError
from urllib.error import HTTPError, URLError

import nltk

from utility.spell_checker import *


class URLOpenWrapper:
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    def __init__(self, page_url):
        self._page_url = page_url

    def __enter__(self):
        try:
            gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            request = urllib.request.Request(
                self._page_url,
                headers={
                    'User-Agent': self.user_agent
                }
            )
            self._response = urllib.request.urlopen(request, context=gcontext)
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
            self._response_code = 0
        except SSLError as e:
            Logger.logger.error("SSL Error : " + self._page_url)
            Logger.logger.error("Reason : " + str(e))
            self._response_code = 0
        except UnicodeEncodeError as e:
            Logger.logger.error("Unicode Error : " + str(e))
            Logger.logger.error("Reason : " + str(e))
            self._response_code = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

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

    def is_successful_response(self):
        return True if self._response_code in successResponse else False


successResponse = [200, 201, 202, 203, 204, 205, 206]
