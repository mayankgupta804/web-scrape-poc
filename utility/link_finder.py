from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.images = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    if '#' in url:
                        rest = self.check_links(url)
                        self.links.add(rest)
                    else:
                        self.links.add(url)
        elif tag == 'img':
            for (attribute, value) in attrs:
                if attribute == 'src':
                    url = parse.urljoin(self.base_url, value)
                    self.images.add(url)

    def check_links(self, url):
        separator = '#'
        rest = url.split(separator, 1)[0]
        return rest

    def page_links(self):
        return self.links

    def image_links(self):
        return self.images

    def error(self, message):
        pass
