import re
from multiprocessing import JoinableQueue
from threading import Thread

import enchant
from enchant.tokenize import get_tokenizer

from utility.counter import Counter
from utility.logger import Logger
from utility.utilities import ignored

q = JoinableQueue()


def add_words_to_queue(page_contents, url):
    page_contents = re.sub(r'\w+\.\.\.\s?', '', page_contents)
    tknzr = get_tokenizer("en_US")
    counts = {}
    for (word, pos) in tknzr(page_contents.lower()):
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    for word, count in counts.items():
        word_dict = {'word': word, 'count': count, 'url': url}
        q.put(word_dict)


class CheckWords(Thread):
    def __init__(self, file_name, mongod):
        Thread.__init__(self)
        self._file = file_name
        self.daemon = True
        self.mongod = mongod

    def run(self):
        chkr = enchant.DictWithPWL("en_US", "resources/words.txt")

        try:
            while True:
                word_dict = q.get()
                with ignored(UnicodeEncodeError):
                    if not chkr.check(word_dict['word']):
                        self.mongod.add_word_to_dictionary(word_dict)
                q.task_done()
                Counter.total_spellings += 1
        except EOFError as e:
            Logger.logger.info("Spell checker EOFError : " + str(e))
