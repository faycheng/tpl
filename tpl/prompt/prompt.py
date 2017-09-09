# -*- coding:utf-8 -*-

import os

import prompt_toolkit

from prompt_toolkit.history import FileHistory
from .completer import *


history = FileHistory(os.path.join(path.HOME, '.templates', 'tpl.history'))


def prompt(message, default=None, multiline=False):
    completer = WordCompleter(words=[], history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return str(res)


def prompt_list(message, default=None, completions=None, multiline=False):
    completer = WordCompleter(words=completions, history=history)
    res = prompt_toolkit.prompt(message, default=default or '', history=history, completer=completer, multiline=multiline)
    return res


def prompt_path(message, root, type='DIR', recursion=False, default=None):
    completer = PathCompleter(root, match_type=type, recursion=False)
    res = prompt_toolkit.prompt(message, default=default or '', completer=completer)
    return res


