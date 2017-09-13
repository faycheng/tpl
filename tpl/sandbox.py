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



DEFAULT_SHELL_VARS = {
    'pipe': None
}


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


# FIXME 需要添加超时支持
def shell_execute(command):
    with path.TempPipe() as tp:
        DEFAULT_SHELL_VARS['pipe'] = tp.pipe_path
        ShellExec(command, DEFAULT_SHELL_VARS).start()
        time.sleep(0.5)
        c = tp.pipe.read()
        c.strip()
        context = json.loads(c)
    return context
