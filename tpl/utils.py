# -*- coding:utf-8 -*-

from functools import wraps
from collections import Iterable


true_strs = ['true', 'yes', 't', 'y']
false_strs = ['false', 'no', 'f', 'n']
bool_strs = true_strs + false_strs


def _iter(obj):
    itered_item = set()
    for item in obj:
        if item not in itered_item:
            itered_item.add(item)
            yield item


def unique(func):
    @wraps(func)
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        if isinstance(res, Iterable):
            return _iter(res)
        return res

    return inner


def str2boo(str, strict=True):
    if str.lower() in true_strs:
        return True
    if str.lower() in false_strs:
        return False
    if strict is True:
        raise ValueError('input({}) must be in {}'.format(str, bool_strs))