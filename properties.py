from configparser import ConfigParser


class Properties:
    def __init__(self):
        self._p = ConfigParser()
        self._p.read("config.properties")

    @property
    def depth(self):
        return int(self._p.get("PROPERTIES", "depth"))

    @property
    def folder(self):
        return self._p.get("PROPERTIES", "folder")

    @property
    def home_page(self):
        return self._p.get("PROPERTIES", "homepage")

    @property
    def threads(self):
        return int(self._p.get("PROPERTIES", "no_of_threads"))

    @property
    def mode(self):
        return self._p.get("PROPERTIES", "mode")

    @property
    def crawled_file(self):
        file = self.folder + "/" + self._p.get("FILES", "crawled")
        return file

    @property
    def queue_file(self):
        file = self.folder + "/" + self._p.get("FILES", "queue")
        return file

    @property
    def spelling_file(self):
        file = self.folder + "/" + self._p.get("FILES", "spelling")
        return file

    @property
    def failed_file(self):
        file = self.folder + "/" + self._p.get("FILES", "failed")
        return file

