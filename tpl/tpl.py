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

    def __init__(self, tpl_dir, output_dir=None):
        self.tpl_dir = tpl_dir
        self.output_dir = output_dir or os.getcwd()

    @property
    def tpl_parent_dir(self):
        return path.get_parent_path(self.tpl_dir, 1)

    def is_ignored_file(self, file):
        file_name = file.split('/')[-1]
        if file_name in self.IGNORE_FILES:
            return True
        return False

    def render_file(self, file, context):
        env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        render_file = file.replace(self.tpl_dir + '/', '')
        if '{{' in render_file and '}}' in render_file:
            render_file = env.from_string(render_file).render(context)
        render_file = os.path.join(self.output_dir, render_file)
        with open(file, 'r') as fd:
            file_content = fd.read()
        render_file_content = env.from_string(file_content).render(context)
        return render_file, render_file_content

    def render_dir(self, dir, context):
        render_dir = dir.replace(self.tpl_dir + '/', '')
        # FIXME 如果存在类似 {{dir1/dir2}} 这样的 path，render 时会出错
        if not ('{{' in render_dir and '}}' in render_dir):
            return os.path.join(self.output_dir, render_dir)
        env = jinja2.Environment(undefined=jinja2.StrictUndefined)
        render_dir = env.from_string(render_dir).render(context)
        render_dir = os.path.join(self.output_dir, render_dir)
        return render_dir

    def render(self, context):
        assert isinstance(context, dict)
        render_dirs = []
        render_files = []
        for dir in path.list_dirs(self.tpl_dir):
            render_dirs.append(self.render_dir(dir, context))
        for file in path.list_files(self.tpl_dir):
            if self.is_ignored_file(file):
                continue
            render_files.append(self.render_file(file, context))
        return render_dirs, render_files
