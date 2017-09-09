# -*- coding:utf-8 -*-

import os
import click
import sys

from tpl import path
from tpl.core import Template
from tpl.constructor import construct_context

TPL_STORAGE_DIR = os.path.join(path.HOME, '.templates')

OFFICIAL_NAMESPACE = 'python-tpl'
SEPARATOR = ':'


def panic_if_path_not_exist(path, type):
    if not os.path.exists(path):
        click.echo('path({}) not exist'.format(path))
        sys.exit(1)
    type_validate = os.path.isdir if type == 'dir' else os.path.isfile
    if not type_validate(path):
        click.echo('path must be {}'.format(type))
        sys.exit(1)


def panic_wich_exit_code(message='', exit_code=1):
    click.echo('{}\texit code:{}'.format(message, exit_code))


def locate_constructor_script(tpl_dir):
    shell_constructor_script = os.path.join(tpl_dir, 'constructor.sh')
    if os.path.exists(shell_constructor_script) and os.path.isfile(shell_constructor_script):
        return shell_constructor_script
    py_constructor_script = os.path.join(tpl_dir, 'constructor.py')
    if os.path.exists(py_constructor_script) and os.path.isfile(py_constructor_script):
        return py_constructor_script


@click.group()
def tpl():
    pass


@tpl.command()
@click.argument('template', type=str)
@click.option('--namespace', type=str, default=OFFICIAL_NAMESPACE)
def pull(namespace, template):
    clone_url = 'https://github.com/{}/{}.git'.format(namespace, template)
    clone_dir = '{}/{}/{}'.format(TPL_STORAGE_DIR, namespace, template)
    clone_command = 'git clone {} {}'.format(clone_url, clone_dir)
    os.system(clone_command)


@tpl.command()
def desc():
    pass


@tpl.command()
def update():
    pass


@tpl.command()
def config():
    pass


@tpl.command()
@click.argument('template', type=str)
@click.option('--namespace', type=str, default=OFFICIAL_NAMESPACE)
@click.option('--branch', type=str, default='')
@click.option('--output_dir', type=str, default=path.CWD)
@click.option('--echo', is_flag=True)
def render(namespace, branch, template, output_dir, echo):
    repo_dir = '{}/{}/{}'.format(TPL_STORAGE_DIR, namespace, template)
    tpl_dir = os.path.join(repo_dir, 'tpl')
    panic_if_path_not_exist(repo_dir, 'dir')
    panic_if_path_not_exist(tpl_dir, 'dir')
    panic_if_path_not_exist(output_dir, 'dir')
    if not (os.path.exists(tpl_dir) and os.path.isdir(tpl_dir)):
        panic_wich_exit_code('tpl dir({}) not exist'.format(tpl_dir), 1)
    check_out_command = 'old_path=$(pwd -P) && cd {};git checkout {} && cd $old_path'.format(repo_dir, branch)
    check_out_exit_code = os.system(check_out_command)
    if check_out_exit_code != 0:
        panic_wich_exit_code('failed to checkout {}'.format(branch), check_out_exit_code)
    constructor_script = locate_constructor_script(tpl_dir)
    if constructor_script is None:
        panic_wich_exit_code('can not find constructor script in {}'.format(tpl_dir), 1)
    context = construct_context(constructor_script)
    tpl = Template(os.path.join(repo_dir, 'tpl'), output_dir)
    rendered_dirs, rendered_files = tpl.render(context)
    for dir in rendered_dirs:
        if echo is True:
            click.echo('render dir: {}'.format(dir))
            break
        path.mkdirs(dir)
    for file, file_content in rendered_files:
        if echo is True:
            click.echo('render file: {}\n{}'.format(file, file_content))
            break
        file_parent_dir = path.get_parent_path(file, 1)
        if not os.path.exists(file_parent_dir):
            path.mkdirs(file_parent_dir)
        with open(file, 'w') as fd:
            fd.write(file_content)
    click.echo('render {}/{}:{} successfully'.format(namespace, template, branch))


if __name__ == '__main__':
    tpl()
