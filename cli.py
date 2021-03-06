# -*- coding:utf-8 -*-

import os
import click
import sys
import ast

from tpl.hook import run_hook
from tpl.core import Template
from tpl.constructor import construct_context
from pykit.path import HOME, CWD
from pykit.path.helper import mkdirs, get_parent_path
from pykit.path.iter import list_dirs
from pykit.path.path import Path

TPL_STORAGE_DIR = os.path.join(HOME, '.templates')

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


def panic_with_exit_code(message='', exit_code=1):
    click.echo('{}\texit code:{}'.format(message, exit_code))
    sys.exit(1)


def locate_constructor_script(repo_dir):
    shell_constructor_script = os.path.join(repo_dir, 'constructor.sh')
    if os.path.exists(shell_constructor_script) and os.path.isfile(
            shell_constructor_script):
        return shell_constructor_script
    py_constructor_script = os.path.join(repo_dir, 'constructor.py')
    if os.path.exists(py_constructor_script) and os.path.isfile(
            py_constructor_script):
        return py_constructor_script


def locate_after_render_hook(repo_dir):
    after_render_hook = os.path.join(repo_dir, 'after_render.sh')
    if os.path.exists(after_render_hook) and os.path.isfile(after_render_hook):
        return after_render_hook


def update_template_repo(tpl_dir):
    if not (os.path.exists(tpl_dir) and os.path.isdir(tpl_dir)):
        click.echo('template repo({}) not exist'.format(tpl_dir))
        return
    update_command = 'old_path=$(pwd -P) && cd {};git pull --all && cd $old_path'.format(
        tpl_dir)
    command_exit_code = os.system(update_command)
    if command_exit_code != 0:
        click.echo('failed to update {}, exit code:{}'.format(
            tpl_dir, command_exit_code))
        return
    click.echo('update {} successfully'.format(tpl_dir))


def literal_eval(text):
    try:
        return ast.literal_eval(text)
    except ValueError:
        return text

def parse_args(ctx):
    args = []
    for text in ctx.args:
        if "--" in text:
            break
        args.append(literal_eval(text))
    return args


def parse_kwargs(ctx):
    kwargs = {}
    k, v = None, None
    for text in ctx.args:
        if "--" in text:
            if "=" in text:
                text = text.strip("-")
                kwargs[text.split("=")[0]] = literal_eval(text.split("=")[-1])
                continue
            k = text.strip("-")
            continue
        if k is not None:
            kwargs[k] = literal_eval(text)
            k = None
            continue
    return kwargs

@click.group()
def tpl():
    """Command line utility for generating files or directories from template"""


@tpl.command(short_help='pull repo of template from github')
@click.argument('template', type=str)
@click.option(
    '--namespace',
    type=str,
    default=OFFICIAL_NAMESPACE,
    help='namespace of template')
def pull(namespace, template):
    """
    \b
    pull repo of template from github
    ex: pull hello_world --namespace python-tpl
    """
    clone_url = 'https://github.com/{}/{}.git'.format(namespace, template)
    clone_dir = '{}/{}/{}'.format(TPL_STORAGE_DIR, namespace, template)
    clone_command = 'git clone {} {}'.format(clone_url, clone_dir)
    os.system(clone_command)


@tpl.command(short_help='show all local templates')
def list():
    """
    \b
    storage path: ~/.templates/
    show all local templates.
    ex: pull hello_world --namespace python-tpl
    """
    from tabulate import tabulate
    npaths = [
        Path(path) for path in list_dirs(TPL_STORAGE_DIR, recursion=False)
        if Path(path).is_dir
    ]
    table = []
    for npath in npaths:
        for tpath in [
                Path(path)
                for path in list_dirs(npath.abs_path, recursion=False)
                if Path(path).is_dir
        ]:
            table.append((npath.name, tpath.name))
    click.echo(tabulate(table, headers=("namespace", "tpl")))


@tpl.command(short_help='update specified template or all templates')
@click.option('--template', type=str, default='', help='name of template')
@click.option(
    '--namespace',
    type=str,
    default=OFFICIAL_NAMESPACE,
    help='namespace of template')
def update(template, namespace):
    """
    \b
    update specified template or all templates
    ex:
    update specified template:                      update hello_world --namespace python-tpl
    update all templates of specified namespace:    update --namespace $YOUR_NAMSPACE
    update all official templates:                  update
    """
    namespace_dir = os.path.join(TPL_STORAGE_DIR, namespace)
    if template:
        update_template_repo(os.path.join(namespace_dir, template))
        sys.exit(0)

    for tpl_repo in list_dirs(namespace_dir, recursion=False):
        update_template_repo(tpl_repo)


@tpl.command(short_help='generate files or dirs to output dir', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('template', type=str)
@click.option(
    '--namespace',
    type=str,
    default=OFFICIAL_NAMESPACE,
    help='namespace of template')
@click.option('--branch', type=str, default='', help='branch of template')
@click.option('--output_dir', type=str, default=CWD, help='output dir in disk')
@click.option(
    '--echo',
    is_flag=True,
    help='flag of echo mode, output_dir will be ignored while echo is specified'
)
@click.option(
    '--anti_ignores', type=str, default='', help='anti-ignored files or dirs')
@click.pass_context
def render(ctx, namespace, branch, template, output_dir, echo, anti_ignores):
    """
    \b
    generate files or dirs to output dir according to specified template
    ex: render hello_world --namespace python-tpl --branch master --output_dir $HOME
    """
    args = parse_args(ctx)
    kwargs = parse_kwargs(ctx)
    repo_dir = '{}/{}/{}'.format(TPL_STORAGE_DIR, namespace, template)
    tpl_dir = os.path.join(repo_dir, 'tpl')
    panic_if_path_not_exist(repo_dir, 'dir')
    panic_if_path_not_exist(tpl_dir, 'dir')
    panic_if_path_not_exist(output_dir, 'dir')
    if not (os.path.exists(tpl_dir) and os.path.isdir(tpl_dir)):
        panic_with_exit_code('tpl dir({}) not exist'.format(tpl_dir), 1)
    if branch:
        check_out_command = 'old_path=$(pwd -P) && cd {};git checkout {} && cd $old_path'.format(
            repo_dir, branch)
        check_out_exit_code = os.system(check_out_command)
        if check_out_exit_code != 0:
            panic_with_exit_code('failed to checkout {}'.format(branch),
                                 check_out_exit_code)
    constructor_script = locate_constructor_script(repo_dir)
    context = {}
    if constructor_script is not None:
        context = construct_context(constructor_script, *args, **kwargs)
    anti_ignores = [
        ignore.strip() for ignore in anti_ignores.split(',') if ignore
    ]
    tpl = Template(
        os.path.join(repo_dir, 'tpl'), output_dir, anti_ignores=anti_ignores)
    rendered_dirs, rendered_files = tpl.render(context)
    for dir in rendered_dirs:
        if echo is True:
            click.echo('render dir: {}'.format(dir))
            break
        mkdirs(dir)
    for file, file_content in rendered_files:
        if echo is True:
            click.echo('render file: {}\n{}'.format(file, file_content))
            continue
        file_parent_dir = get_parent_path(file, 1)
        if not os.path.exists(file_parent_dir):
            mkdirs(file_parent_dir)
        with open(file, 'w') as fd:
            fd.write(file_content)
    click.echo('render {}/{}:{} successfully'.format(namespace, template,
                                                     branch))
    after_render_hook = locate_after_render_hook(repo_dir)
    if after_render_hook:
        run_hook(after_render_hook)


if __name__ == '__main__':
    tpl()
