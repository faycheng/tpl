# -*- coding:utf-8 -*-

import os
from tpl.render import render
from tpl.ignore import parse_rules, is_ignored
from candy.path.helper import get_parent_path
from candy.path.iter import list_dirs, list_files


class Template(object):
    IGNORE_RULRS = [
        '__pycache__',
        '.vscode',
        '*.pyc'
    ]

    def __init__(self, tpl_dir, output_dir=None, anti_ignores=None):
        self.tpl_dir = tpl_dir
        self.anti_ignores = anti_ignores or []
        self.output_dir = output_dir or os.getcwd()

    @property
    def tpl_parent_dir(self):
        return get_parent_path(self.tpl_dir, 1)

    @property
    def ignore_rules(self):
        work_dir = get_parent_path(self.tpl_dir, 1)
        rules = parse_rules(self.IGNORE_RULRS, self.tpl_parent_dir)
        ignore_file = os.path.join(work_dir, 'ignores')
        if os.path.exists(ignore_file) and os.path.isfile(ignore_file):
            rules.extend(parse_rules(ignore_file, self.tpl_parent_dir))
        return rules

    def is_ignored_dir(self, dir):
        dir_name = dir.split('/')[-1]
        if dir_name in self.anti_ignores:
            return False
        if dir_name in self.IGNORE_DIRS:
            return True
        return False

    def is_ignored_file(self, file):
        file_name = file.split('/')[-1]
        if file_name in self.anti_ignores:
            return False
        if file_name in self.IGNORE_FILES:
            return True
        if file_name.endswith('.pyc'):
            return True
        return False

    def is_ignored(self, path):
        for ir in self.ignore_rules:
            if ir.match(path):
                return True
        return False

    def render_file(self, file, context):
        render_file = file.replace(self.tpl_dir + '/', '')
        if '{{' in render_file and '}}' in render_file:
            render_file = render(render_file, context)
        render_file = os.path.join(self.output_dir, render_file)
        with open(file, 'r') as fd:
            file_content = fd.read()
        render_file_content = render(file_content, context)
        return render_file, render_file_content

    def render_dir(self, dir, context):
        render_dir = dir.replace(self.tpl_dir + '/', '')
        # FIXME 如果存在类似 {{dir1/dir2}} 这样的 path，render 时会出错
        if not ('{{' in render_dir and '}}' in render_dir):
            return os.path.join(self.output_dir, render_dir)
        render_dir = render(render_dir, context)
        render_dir = os.path.join(self.output_dir, render_dir)
        return render_dir

    def render(self, context):
        assert isinstance(context, dict)
        render_dirs = []
        render_files = []
        for dir in list_dirs(self.tpl_dir):
            if self.is_ignored(dir):
                continue
            render_dirs.append(self.render_dir(dir, context))
        for file in list_files(self.tpl_dir):
            if self.is_ignored(file):
                continue
            render_files.append(self.render_file(file, context))
        return render_dirs, render_files
