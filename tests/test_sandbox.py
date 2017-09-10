import pytest

from unittest import mock
from .faker import *
from tpl.sandbox import py_execute, shell_execute


def test_py_execute():
    command = '{"key":"value"}'
    context = py_execute(command)
    assert isinstance(context, dict)
    assert context.get('key') == 'value'



def test_shell_execute():
    pass