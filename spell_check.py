from multiprocessing import JoinableQueue
from threading import Thread

import enchant
from enchant.tokenize import get_tokenizer

from utilities import append_to_file

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
        chkr = enchant.DictWithPWL("en_US", "words.txt")
        while True:
            dict = q.get()
            try:
                if not chkr.check(dict['word']):
                    append_to_file(self._file, dict['word'] + "," + str(dict['count']) + "," + dict['url'])
            except UnicodeEncodeError:
                pass
            finally:
                q.task_done()
