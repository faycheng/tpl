# -*- coding:utf-8 -*-

from prompt_toolkit.validation import Validator, ValidationError


class StrValidator(Validator):
    def validate(self, document):
        pass


class IntValidator(Validator):
    def validate(self, document):
        text = document.text
        for index, char in enumerate(text):
            if not char.isdigit():
                raise ValidationError(message='Input contains non-numeric char', cursor_position=index)





