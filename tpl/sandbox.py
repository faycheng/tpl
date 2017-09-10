# -*- coding:utf-8 -*-

import os
import sys
import time
import json
import threading
import delegator
from tpl import path
from tpl import prompt
from tpl import errors


DEFAULT_PY_GLOBALS = {
    'os': os,
    'sys': sys,
    'json': json,
    'path': path,
    'mdfifo': os.mkfifo,
    'prompt': prompt
}

DEFAULT_PY_LOCALS = {
    'context_pipe': None
}

DEFAULT_SHELL_VARS = {
    'pipe': None
}


class PyExec(threading.Thread):
    def __init__(self, command, injected_globals, injected_locals):
        self.command = command
        self.injected_globals = injected_globals
        self.injected_locals = injected_locals
        super(PyExec, self).__init__(name='py_exec_tpl_constructor')

    def run(self):
        exec(self.command, self.injected_globals, self.injected_locals)


def py_execute(command, injected_globals=None, injected_locals=None):
    injected_globals = injected_globals or {}
    injected_locals = injected_locals or {}
    injected_globals.update(DEFAULT_PY_GLOBALS)
    with path.TempPipe() as tp:
        DEFAULT_PY_LOCALS['context_pipe'] = tp.pipe_path
        injected_locals.update(DEFAULT_PY_LOCALS)
        command = 'context={};pipe=open(context_pipe, "w");pipe.write(json.dumps(context));pipe.close()'.format(command)
        PyExec(command, injected_globals, injected_locals).start()
        context = json.loads(tp.pipe.read())
    return context


class ShellExec(threading.Thread):
    def __init__(self, command, injected_vars=None):
        self.command = command
        self.injected_vars = injected_vars
        super(ShellExec, self).__init__(name='shell_exec_tpl_constructor')

    def run(self):
        command = self.command
        for key, value in self.injected_vars.items():
            command = ' && '.join([
                '{}={}'.format(key, value),
                command
            ])
        command_res = delegator.run(command, block=True)
        if command_res.return_code != 0:
            raise errors.ShellExecError(command_res.return_code,
                                        command_res.out,
                                        command_res.err)


def shell_execute(command):
    with path.TempPipe() as tp:
        DEFAULT_SHELL_VARS['pipe'] = tp.pipe_path
        ShellExec(command, DEFAULT_SHELL_VARS).start()
        time.sleep(0.5)
        c = tp.pipe.read()
        c.strip()
        context = json.loads(c)
    return context
