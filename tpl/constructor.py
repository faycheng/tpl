# -*- coding:utf-8 -*-
import os
import sys
import uuid
import delegator


sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from tpl import path
from tpl import errors
from tpl import sandbox



def construct_context_from_shell(source):
    assert os.path.exists(source) and os.path.isfile(source)
    command = 'source {}'.format(source)
    return sandbox.shell_execute(command)


def construct_context_from_py():
    pass


def construct_context_from_json():
    pass


def construct_context(type, source):
    pass





