# -*- coding:utf-8 -*-
import os
import sys
import stat
import subprocess

from tpl.errors import HookExecError


def make_executable(hook_path):
    stats = os.stat(hook_path)
    os.chmod(hook_path, stats | stat.S_IEXEC)


def run_hook(hook_path, cwd='.'):
    if hook_path.endswith('.py'):
        command = [sys.executable, hook_path]
    else:
        command = [hook_path]

    make_executable(hook_path)

    proc = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd
    )

    exit_code = proc.wait()
    if exit_code != 0:
        raise HookExecError(exit_code)


