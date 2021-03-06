# -*- coding:utf-8 -*-
import os
import sys
import gettext
from tpl import sandbox
from pykit.path.helper import get_parent_path

_ = gettext.gettext


def construct_context_from_shell(source):
    assert os.path.exists(source) and os.path.isfile(source)
    command = 'source {}'.format(source)
    return sandbox.shell_execute(command)


def construct_context_from_py(source, *args, **kwargs):
    if not (os.path.exists(source) and os.path.isfile(source)):
        return {}
    source_name = source.split('/')[-1][:-3]
    sys.path.insert(0, get_parent_path(source, 1))
    try:
        context = __import__(source_name).construct(*args, **kwargs)
    finally:
        sys.path.remove(get_parent_path(source, 1))
    return context


def construct_context_from_json():
    pass


# TODO refactor construct context from shell
def construct_context(source, *args, **kwargs):
    assert isinstance(source, str)
    # if source.endswith('.sh'):
    #     return construct_context_from_shell(source)
    if source.endswith('.py'):
        return construct_context_from_py(source, *args, **kwargs)
    raise TypeError(_('Constructor type is invalid.Source file must be endswith ".py"'))


