# -*- coding:utf-8 -*-

from functools import wraps
from collections import Iterable


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

