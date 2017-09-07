# -*- coding:utf-8 -*-
import os
import sys
import uuid
import delegator


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tpl import path
from tpl import errors


def construct_context_from_shell(source):
    assert os.path.exists(source) and os.path.isfile(source)
    tmp_file_path = os.path.join(os.path.expanduser('~'), '.templates', str(uuid.uuid4()))
    assets_dir = '{}/assets'.format(path.get_parent_path(os.path.abspath(__file__), 2))
    command = ' && '.join([
        'source {}/{}'.format(assets_dir, 'export_alias.sh'),
        'source {}'.format(source),
        'python {}/{} {}'.format(assets_dir, 'save_tpl_envs.py', tmp_file_path)
    ])
    command_res = delegator.run(command)
    if command_res.return_code != 0:
        raise errors.ShellExecError(command_res.return_code,
                                    command_res.out,
                                    command_res.err)


def construct_context_from_py():
    pass


def construct_context_from_json():
    pass


def construct_context(type, source):
    pass





