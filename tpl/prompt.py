# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import prompt_toolkit

from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completion, Completer
from tpl import path


history = FileHistory(os.path.join(path.HOME, '.templates', 'tpl.history'))


class WordMatchType(object):
    CONTAINS = 'CONTAINES'
    STARTSWITH = 'STARTSWITH'


class WordCompleter(Completer):
    def __init__(self, words=None, history=None, match_type=WordMatchType.CONTAINS):
        self.words = words or []
        self.history = history or []
        self.match_type = match_type

    def match(self, word_before_cursor, word):
        if self.match_type == WordMatchType.CONTAINS:
            return word_before_cursor in word

    def get_completions(self, document, complete_event):
        word_before_cursor = document.text_before_cursor.lower()
        for word in self.words:
            if self.match(word_before_cursor, word):
                display_meta = '    custom'
                yield Completion(word, -len(word_before_cursor), display_meta=display_meta)
        for record in self.history:
            if self.match(word_before_cursor, record):
                display_meta = '    history'
                yield Completion(record, -len(word_before_cursor), display_meta=display_meta)


def prompt(message, type=None, default=None, completer=None, multiline=False):
    pass


def prompt_list():
    pass


def prompt_path():
    pass
