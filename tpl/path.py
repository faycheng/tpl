# -*- coding:utf-8 -*-

import os
import uuid


class TempDir(object):
    pass


class TempFile(object):
    pass


class TempPipe(object):
    def __init__(self):
        self.pipe_path = '/tmp/{}.pipe'.format(str(uuid.uuid4()))
        self.pipe = None

    def __enter__(self):
        os.mkfifo(self.pipe_path)
        self.pipe = open(self.pipe_path, 'r')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pipe.close()
        os.remove(self.pipe_path)


def list_dirs(path):
    assert os.path.exists(path) and os.path.isdir(path)
    for dir_path, dir_names, _ in os.walk(path):
        for dir_name in dir_names:
            yield os.path.join(dir_path, dir_name)


def list_files(path):
    assert os.path.exists(path) and os.path.isdir(path)
    for dir_path, _, file_names in os.walk(path):
        for file_name in file_names:
            yield os.path.join(dir_path, file_name)


def list_all(path):
    assert os.path.exists(path) and os.path.isdir(path)
    for dir in list_dirs(path):
        yield dir
    for file in list_files(path):
        yield file


def get_parent_path(path, depth=1):
    parent_path = path
    for _ in range(depth):
        parent_path = os.path.abspath(os.path.dirname(parent_path))
    return parent_path