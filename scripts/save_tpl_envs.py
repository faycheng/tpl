# -*- coding:utf-8 -*-

import os
import sys
import json


def save_tpl_envs(path):
    envs = {}
    for key, value in os.environ.items():
        if key.startswith('TPL_'):
            envs[key[4:]] = value
    with open(path, 'w') as fd:
        fd.write(json.dumps(envs))


if __name__ == '__main__':
    path = sys.argv[1]
    save_tpl_envs(path)
