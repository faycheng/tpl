# -*- coding:utf-8 -*-

import pytest

from tpl import ignore
from candy.utils.faker import random_string
from candy.path.temp import TempFile


def test_split_path():
    work_dir = '/Users/root'
    rule = 'tpl'
    ir = ignore.IgnoreRule(rule, work_dir)

    path = '{}/templates/tpl'.format(work_dir)
    sp = ir.split_path(path)
    assert len(sp) == 2
    assert 'templates' in sp
    assert 'tpl' in sp

    sp = ir.split_path(work_dir)
    assert len(sp) == 0

    path = '{}/  / '.format(work_dir)
    sp = ir.split_path(path)
    assert len(sp) == 0


def test_match():
    work_dir = '/Users/root'
    rule = 'tpl'
    ir = ignore.IgnoreRule(rule, work_dir)

    path = '{}/templates/tpl'.format(work_dir)
    assert ir.match(path) is True

    path = '{}/{}'.format(work_dir, random_string())
    assert ir.match(path) is False

    work_dir = '/Users/root'
    rule = '*tpl'
    ir = ignore.IgnoreRule(rule, work_dir)

    path = '{}/{}_tpl'.format(work_dir, random_string())
    assert ir.match(path) is True
