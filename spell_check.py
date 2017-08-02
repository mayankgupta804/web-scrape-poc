from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer, URLFilter, EmailFilter
from multiprocessing import JoinableQueue
from threading import Thread

from general import append_to_file

q = JoinableQueue(10000)


def add_words_to_queue(page_contents, url):
    tknzr = get_tokenizer("en_US")
    counts = {}
    for (word, pos) in tknzr(page_contents.lower()):
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    for word, count in counts.items():
        dict = {'word': word, 'count': count, 'url': url}
        q.put(dict)


class CheckWords(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self._file = file_name

    def run(self):
        chkr = SpellChecker("en_US", filters=[EmailFilter, URLFilter])
        while True:
            dict = q.get(True, 60)
            try:
                if not chkr.check(dict['word']):
                    append_to_file(self._file, dict['word'] + "," + str(dict['count']) + "," + dict['url'])
            except UnicodeEncodeError:
                pass
            except:
                pass
