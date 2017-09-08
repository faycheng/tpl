# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import prompt_toolkit

from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.validation import Validator, ValidationError
from tpl import path
from tpl import utils


class WordMatchType(object):
    CONTAINS = 'CONTAINES'
    STARTSWITH = 'STARTSWITH'


class WordCompleter(Completer):
    def __init__(self, words=None, history=None, match_type=WordMatchType.CONTAINS):
        self.words = words or []
        self.history = history or []
        self.match_type = match_type
        self.lower = False

    def match(self, text_before_cursor, word):
        if self.match_type == WordMatchType.CONTAINS:
            return text_before_cursor in word

    # utils unique 只能保证 custome & history 各自的列表中不出现重复，无法保证 custom & history 没有交集
    @utils.unique
    def get_completions(self, document, complete_event):
        if self.lower is False:
            self.words = [word.lower() for word in self.words]
            self.history = [record.lower() for record in self.history]
            self.lower = True
        text_before_cursor = document.text_before_cursor.lower()
        for word in self.words:
            if self.match(text_before_cursor, word):
                display_meta = '    custom'
                yield Completion(word, -len(text_before_cursor), display_meta=display_meta)
        for record in self.history:
            if self.match(text_before_cursor, record):
                display_meta = '    history'
                yield Completion(record, -len(text_before_cursor), display_meta=display_meta)


class PathMatchType(object):
    DIRS = 'DIRS'
    FILES = 'FILES'
    ALL = 'ALL'


class PathCompleter(Completer):
    def __init__(self, root, match_type=PathMatchType.ALL, recursion=False):
        self.root = root
        self.match_type = match_type
        self.recursion = recursion

    # TODO 去重
    @utils.unique
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor.lower()
        list_paths = path.list_all
        if self.match_type == PathMatchType.DIRS:
            list_paths = path.list_dirs
        if self.match_type == PathMatchType.FILES:
            list_paths = path.list_files
        if self.match_type == PathMatchType.ALL:
            list_paths = path.list_all
        for p in list_paths(self.root, recursion=self.recursion):
            if text_before_cursor in p.lower():
                yield Completion(p, start_position=-len(text_before_cursor), display_meta=self.match_type)
            p_name = p.rstrip('/').split('/')[-1]
            if text_before_cursor in p_name.lower():
                yield Completion(p, start_position=-len(text_before_cursor), display_meta=self.match_type)


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not (text and text.isdigit):
            return
        for index, char in enumerate(text):
            if not char.isdigit():
                raise ValidationError(message='Input contains non-numeric char', cursor_position=index)


history = FileHistory(os.path.join(path.HOME, '.templates', 'tpl.history'))


def prompt_str(message, default=None, multiline=False):
    completer = WordCompleter(words=[], history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return str(res)


def prompt_number(message, default=None):
    res = prompt_toolkit.prompt(message, default=default or '', history=history, validator=NumberValidator())
    return int(res)


def prompt_list(message, default=None, completions=None, multiline=False):
    completer = WordCompleter(words=completions, history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return res


def prompt_path(message, root, type='DIR', recursion=False, default=None):
    completer = PathCompleter(root, match_type=type, recursion=False)
    res = prompt_toolkit.prompt(message, default=default or '', completer=completer)
    return res


