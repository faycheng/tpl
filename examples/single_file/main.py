# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from tpl.tpl import Template
from tpl import path
from tpl import constructor


def main():
    cwd = path.get_parent_path(os.path.abspath(__file__), 1)
    tpl_dir = os.path.join(cwd, 'template')
    context = constructor.construct_context_from_shell(os.path.join(tpl_dir, 'construct.sh'))
    t = Template(tpl_dir, os.path.join(path.get_parent_path(os.path.abspath(__file__), 1), 'tpl_res'))
    render_dirs, render_files = t.render(context)
    for dir in render_dirs:
        path.mkdirs(dir)
    for file, file_content in render_files:
        file_parent_dir = path.get_parent_path(file, 1)
        if not os.path.exists(file_parent_dir):
            path.mkdirs(file_parent_dir)
        with open(file, 'w') as fd:
            fd.write(file_content)

if __name__ == '__main__':
    main()
