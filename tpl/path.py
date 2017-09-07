# -*- coding:utf-8 -*-

import os


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
    pass

