# -*- coding:utf-8 -*-

import jinja2
from candy.prompt.prompt import prompt

env = jinja2.Environment(undefined=jinja2.StrictUndefined)


def render(tpl_text, context):
    try:
        return env.from_string(tpl_text).render(context)
    except jinja2.UndefinedError as e:
        undefined_var = e.message[1:-14]
        value = prompt('{}: '.format(undefined_var))
        context.setdefault(undefined_var, value)
        return render(tpl_text, context)
