# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import prompt_toolkit

from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completion
from prompt_toolkit.contrib.completers import WordCompleter
from tpl import path


history = FileHistory(os.path.join(path.HOME, '.templates', 'tpl.history'))


class WordCompleterWithHistory(WordCompleter):
    def __init__(self, words=None, *args, **kwargs):
        words = words or []
        super(WordCompleterWithHistory, self).__init__(words, *args, **kwargs)

    def word_matches(self, word_before_cursor, word):
        """ True when the word before the cursor matches. """
        if self.ignore_case:
            word = word.lower()

        if self.match_middle:
            return word_before_cursor in word
        else:
            return word.startswith(word_before_cursor)

    def get_completions(self, document, complete_event):
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(WORD=self.WORD)

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        for completion in super(WordCompleterWithHistory, self).get_completions(document, complete_event):
            yield completion
        for record in history:
            if self.word_matches(word_before_cursor, record):
                display_meta = self.meta_dict.get(record, '')
                yield Completion(record, -len(word_before_cursor), display_meta=display_meta)


def prompt(message, type=None, default=None, completer=None, multiline=False):
    pass


def prompt_list():
    pass


def prompt_path():
    pass

