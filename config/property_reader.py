from configparser import ConfigParser, NoOptionError

import os

import sys


class PropertyReader:

    def __init__(self, file="config.properties"):
        self._p = ConfigParser()
        self._p.read(file)

    @property
    def depth(self):
        return self._p.getint("PROPERTIES", "depth", fallback=4)

    @property
    def folder(self):
        return self._p.get("PROPERTIES", "folder", fallback="test")

    @property
    def home_page(self):
        try:
            return self._p.get("PROPERTIES", "homepage")
        except NoOptionError as e:
            print(e)
            sys.exit(1)

    @property
    def threads(self):
        return self._p.getint("PROPERTIES", "no_of_threads", fallback=10)

    @property
    def spell_check(self):
        return self._p.getboolean("PROPERTIES", "spell_check", fallback=False)

    @property
    def image_check(self):
        return self._p.getboolean("PROPERTIES", "image_check", fallback=False)

    @property
    def mode(self):
        return self._p.get("PROPERTIES", "mode", fallback="normal")

    @property
    def device(self):
        return self._p.get("PROPERTIES", "device", fallback=None)
