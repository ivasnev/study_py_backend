# coding: utf-8


class AppException(Exception):
    def __init__(self, fieldname="", message=""):
        self.fieldname = fieldname
        self.message = message

    def __str__(self):
        return "fieldname: %s, message: %s" % (self.fieldname, self.message)


class LogicException(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class ValidationFailure(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class DisplayFailure(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class NameTypeError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class DbError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class FormationError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class FilterError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class ReportError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class RuntimeException(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class SendException(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class ConfigError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)


class FileError(AppException):
    def __init__(self, fieldname="", message=""):
        super().__init__(fieldname, message)
