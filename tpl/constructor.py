# -*- coding:utf-8 -*-
import os
import sys
import gettext
from tpl import path
from tpl import sandbox

_ = gettext.gettext


def construct_context_from_shell(source):
    assert os.path.exists(source) and os.path.isfile(source)
    command = 'source {}'.format(source)
    return sandbox.shell_execute(command)


def construct_context_from_py(source):
    assert os.path.exists(source) and os.path.isfile(source)
    source_name = source.split('/')[-1][:-3]
    sys.path.insert(0, path.get_parent_path(source, 1))
    try:
        construct = __import__(source_name).construct
        context = construct()
    finally:
        sys.path.remove(path.get_parent_path(source, 1))
    return context


def construct_context_from_json():
    pass


def construct_context(source):
    assert isinstance(source, str)
    if source.endswith('.sh'):
        return construct_context_from_shell(source)
    if source.endswith('.py'):
        return construct_context_from_py(source)
    raise TypeError(_('Constructor type is invalid.Source file must be endswith ".sh", ".py"'))


