# -*- coding:utf-8 -*-

import os
import sys
import jinja2


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.join(__file__))))


env = jinja2.Environment(undefined=jinja2.StrictUndefined)


from tpl.prompt import prompt_str


# TODO prompt 需要能够支持更多类型，比如 dict
def render(tpl_text, context):
    try:
        return env.from_string(tpl_text).render(context)
    except jinja2.UndefinedError as e:
        undefined_var = e.message[1:-14]
        value = prompt_str('{}:'.format(undefined_var))
        context.setdefault(undefined_var, value)
        return render(tpl_text, context)
