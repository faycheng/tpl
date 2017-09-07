# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import jinja2
from tpl import path
from tpl import errors


class Template(object):
    IGNORE_FILES = [
        'construct.sh',
        'construct.py'
    ]

    def __init__(self, tpl_dir):
        self.tpl_dir = tpl_dir

    def is_ignored_file(self, file):
        file_name = file.split('/')[-1]
        if file_name in self.IGNORE_FILES:
            return True
        return False

    def render_file(self, file, context):
        env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        if '{{' in file and '}}' in file:
            file = env.from_string(file).render(context)
        with open(file, 'r') as fd:
            file_content = fd.read()
        file_content = env.from_string(file_content).render(context)
        return file, file_content

    def render_dir(self, dir, context):
        if not ('{{' in dir and '}}' in dir):
            return dir
        env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        dir = env.from_string(dir).render(context)
        return dir

    def render(self, context):
        pass
