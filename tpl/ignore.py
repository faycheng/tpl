# -*- coding:utf-8 -*-

import fnmatch

from candy.path.helper import get_parent_path


class IgnoreRule(object):
    def __init__(self, rule, work_dir):
        self.rule = rule
        self.work_dir = work_dir

    def split_path(self, path):
        path = path.strip()
        path = path.replace(self.work_dir, '')
        return [p.strip() for p in path.split('/') if p.strip()]

    def match(self, path):
        assert path.startswith(self.work_dir)
        for p in self.split_path(path):
            if fnmatch.fnmatch(p, self.rule):
                return True
        return False


def parse_rules(source):
    rules = []
    for line in open(source):
        assert isinstance(line, str)
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        if len(line.split(' ')) > 1:
            continue
        rules.append(IgnoreRule(line, get_parent_path(source, 1)))
    return rules


def is_ignored(rules, data):
    for rule in rules:
        if rule.match(data):
            return True
    return False
