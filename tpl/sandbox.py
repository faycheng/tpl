# -*- coding:utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uuid
import json
import threading
from tpl import path
from tpl import prompt


DEFAULT_GLOBALS = {
    'os': os,
    'sys': sys,
    'json': json,
    'path': path,
    'mdfifo': os.mkfifo,
    'prompt': prompt
}

DEFAULT_LOCALS = {
    'context_pipe': None
}


class PyExec(threading.Thread):
    def __init__(self, command, injected_globals, injected_locals):
        self.command = command
        self.injected_globals = injected_globals
        self.injected_locals = injected_locals
        super(PyExec, self).__init__(name='exec_tpl_constructor')

    def run(self):
        exec(self.command, self.injected_globals, self.injected_locals)


def py_execute(command, injected_globals=None, injected_locals=None):
    injected_globals = injected_globals or {}
    injected_locals = injected_locals or {}
    injected_globals.update(DEFAULT_GLOBALS)
    pipe_path = '/tmp/{}.pipe'.format(str(uuid.uuid4()))
    os.mkfifo(pipe_path)
    DEFAULT_LOCALS['context_pipe'] = pipe_path
    injected_locals.update(DEFAULT_LOCALS)
    command = 'pipe=open(context_pipe, "w");pipe.write(json.dumps({}));pipe.close()'.format(command)
    PyExec(command, injected_globals, injected_locals).start()
    pipe = open(pipe_path)
    context = json.loads(pipe.read())
    pipe.close()
    return context


