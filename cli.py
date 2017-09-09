# -*- coding:utf-8 -*-

import os
import click
import sys

from tpl import path

TPL_DIR = os.path.join(path.HOME, '.templates')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('template', type=str)
@click.option('--namespace', type=str, default='python-tpl')
def pull(template, namespace):
    clone_url = 'https://github.com/{}/{}.git'.format(namespace, template)
    clone_dir = '{}/{}/{}'.format(TPL_DIR, namespace, template)
    clone_command = 'git clone {} {}'.format(clone_url, clone_dir)
    os.system(clone_command)


if __name__ == '__main__':
    cli()