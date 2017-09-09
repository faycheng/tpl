# -*- coding:utf-8 -*-

import os

from enum import Enum
import prompt_toolkit

from prompt_toolkit.history import FileHistory
from .completer import *


history = FileHistory(os.path.join(path.HOME, '.templates', 'tpl.history'))


class PromptType(Enum):
    STR = str
    INT = int
    BOOL = bool
    FLOAT = float
    LIST = list
    DICT = dict
    DIR = str
    FILE = str


def prompt(message, type='STR', default=None, multiline=False):
    assert hasattr(PromptType, type)
    completer = WordCompleter(words=[], history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return getattr(PromptType, type)(res)


def prompt_list(message, type='STR', default=None, completions=None, multiline=False):
    assert hasattr(PromptType, type)
    completer = WordCompleter(words=completions, history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return getattr(PromptType, type)(res)


def prompt_path(message, root, type='DIR', recursion=False, default=None):
    assert hasattr(PromptType, type)
    completer = PathCompleter(root, match_type=type, recursion=recursion)
    res = prompt_toolkit.prompt(message, default=default or '', completer=completer)
    return getattr(PromptType, type)(res)

