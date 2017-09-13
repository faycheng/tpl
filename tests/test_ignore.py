# -*- coding:utf-8 -*-

from tpl import ignore
from candy_path.helper import get_parent_path
from candy_utils.faker import random_string
from candy_path.temp import TempFile


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


def test_parse_rules():
    source = """
    # comment
       
    *tpl
    ?tpl
    """
    with TempFile() as f:
        f.fd.write(source)
        f.close()
        rules = ignore.parse_rules(open(f.path), get_parent_path(f.path, 1))
        assert len(rules) == 2
        for rule in rules:
            assert isinstance(rule, ignore.IgnoreRule)
            assert rule.rule in ['*tpl', '?tpl']


