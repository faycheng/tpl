# -*- coding:utf-8 -*-

from gettext import gettext as _


class BaseError(BaseException):
    ERR_MSG = _('')


class ShellExecError(BaseError):
    ERR_MSG = _('Command exit code not zero. \nExit Code:\n{}.\nOut:\n{}\nErr:\n{}')

    def __init__(self, exit_code, out, err):
        self.message = self.ERR_MSG.format(exit_code, out, err)
        super(ShellExecError, self).__init__(self.message)


class HookExecError(BaseError):
    ERR_MSG = _('Failed to exec hook. \nExit Code:\n{}.')

    def __init__(self, exit_code):
        self.message = self.ERR_MSG.format(exit_code)
        super(HookExecError, self).__init__(self.message)

