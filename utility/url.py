from urllib.parse import urlparse, urldefrag, urlunparse, unquote_plus

from config.properties import Properties
from utility.domain_extractor import get_domain_name


class Url(object):

    def __init__(self, url):
        try:
            self._url = urldefrag(url).url.rstrip('/')
        except AttributeError:
            pass
        parts = urlparse(url)
        parts = parts._replace(query=frozenset())
        self._clean_url = urlunparse(parts)

    def _check_domain(self):
        if get_domain_name(self.clean_url) == get_domain_name(Properties.home_page):
            return True
        return False

    def _check_unicode_char(self):
        try:
            self.clean_url.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False

    def get_filtered_url(self):
        if self._check_domain() and self._check_unicode_char():
            return self._clean_url
        return None

    @property
    def url(self):
        return self._url

    @property
    def clean_url(self):
        return self._clean_url

    def __str__(self):
        return self._url
