from configparser import ConfigParser


class Properties:
    def __init__(self, file="config.properties"):
        self._p = ConfigParser()
        self._p.read(file)

    @property
    def depth(self):
        return self._p.getint("PROPERTIES", "depth",fallback=4)

    @property
    def folder(self):
        return self._p.get("PROPERTIES", "folder",fallback="test")

    @property
    def home_page(self):
        return self._p.get("PROPERTIES", "homepage",fallback="http://www.testvagrant.com")

    @property
    def threads(self):
        return self._p.getint("PROPERTIES", "no_of_threads",fallback=10)

    @property
    def mode(self):
        return self._p.get("PROPERTIES", "mode",fallback="normal")

    @property
    def crawled_file(self):
        file = self.folder + "/" + self._p.get("FILES", "crawled",fallback="crawled.txt")
        return file

    @property
    def queue_file(self):
        file = self.folder + "/" + self._p.get("FILES", "queue",fallback="queue.txt")
        return file

    @property
    def spelling_file(self):
        file = self.folder + "/" + self._p.get("FILES", "spelling",fallback="spelling.txt")
        return file

    @property
    def failed_file(self):
        file = self.folder + "/" + self._p.get("FILES", "failed",fallback="failed.txt")
        return file

