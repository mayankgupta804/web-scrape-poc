from urllib.parse import urlparse, urldefrag, urlunparse


class Url(object):

    def __init__(self, url):
        self._url = urldefrag(url).url.rstrip('/')
        parts = urlparse(url)
        parts = parts._replace(query=frozenset())
        self._clean_url = urlunparse(parts)

    @property
    def url(self):
        return self._url

    @property
    def clean_url(self):
        return self._clean_url

    def __str__(self):
        return self._url
