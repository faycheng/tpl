# -*- coding:utf-8 -*-

from tpl import path
from tpl import utils
from prompt_toolkit.completion import Completion, Completer


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

    # utils unique 只能保证 custom & history 各自的列表中不出现重复，无法保证 custom & history 没有交集
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
