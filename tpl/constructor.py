# -*- coding:utf-8 -*-
import os
import sys
import gettext
import copy
from tpl import path
from tpl import sandbox

_ = gettext.gettext


try:
    import __builtin__ as builtins
except ImportError:
    import builtins


def construct_context_from_shell(source):
    assert os.path.exists(source) and os.path.isfile(source)
    command = 'source {}'.format(source)
    return sandbox.shell_execute(command)


def construct_context_from_py(source):
    assert os.path.exists(source) and os.path.isfile(source)
    injected_locals = {}
    source_name = source.split('/')[-1].split('.')[0]
    try:
        sys.path.insert(0, path.get_parent_path(source, 1))
        construct = __import__(source_name).construct
    finally:
        sys.path.remove(path.get_parent_path(source, 1))
    injected_locals.setdefault('construct', construct)
    command = "construct()"
    context = sandbox.py_execute(command, injected_locals=injected_locals)
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


