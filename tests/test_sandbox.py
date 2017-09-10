import pytest

from unittest import mock
from .faker import *
from tpl.sandbox import shell_execute


def test_shell_execute():
    command = """echo '{"key":"value"}' >> $pipe"""
    context = shell_execute(command)
    assert isinstance(context, dict)
