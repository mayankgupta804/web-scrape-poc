import nltk
import urllib3
from urllib3.connection import UnverifiedHTTPSConnection
from urllib3.exceptions import MaxRetryError, LocationParseError

from utility.spell_checker import *


class URLOpenWrapper:
    user_agent = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    def __init__(self, page_url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._page_url = page_url

    def __enter__(self):
        try:
            self.http = urllib3.PoolManager(headers=URLOpenWrapper.user_agent)
            self.http.ConnectionCls = UnverifiedHTTPSConnection
            self._response = self.http.request('GET', self._page_url)
            self._response_code = self._response.status
        except (UnicodeEncodeError, MaxRetryError, LocationParseError) as e:
            Logger.logger.error("Unicode Encode Error : " + str(e))
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
        return int(self._response.headers['Content-Length'])

    def is_successful_response(self):
        return True if self._response_code in successResponse else False


successResponse = [200, 201, 202, 203, 204, 205, 206]
