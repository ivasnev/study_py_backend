# coding=utf-8
# -*- coding: utf-8 -*-
from pyramid.httpexceptions import HTTPException


class BaseHhtpException(HTTPException):
    """

        Базовый класс ислючений
        Отдаёт страницу с 400 статусом и title = 'Service problem'

    """
    def __init__(self, **kwargs):
        HTTPException.__init__(self)
    code = 400
    title = 'Service problem'