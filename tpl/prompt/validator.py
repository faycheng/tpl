# -*- coding:utf-8 -*-

from prompt_toolkit.validation import Validator, ValidationError


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if not (text and text.isdigit):
            return
        for index, char in enumerate(text):
            if not char.isdigit():
                raise ValidationError(message='Input contains non-numeric char', cursor_position=index)
