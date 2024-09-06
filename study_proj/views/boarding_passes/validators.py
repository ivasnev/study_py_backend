# -*- coding: utf-8 -*-
import json
from typing import Any, Callable
from colander import (Length, MappingSchema,
                      SchemaNode, String, drop, Integer)


# ----------------------------------------------- Общие методы валидации -----------------------------------------------


def request_validator(section: str) -> Callable:
    """Метод валидации параметров запроса"""
    schema = get_validation_schema(section)

    def _request_validator(request, **kwargs) -> None:
        request.validated.update(
            {"filters": schema().bind(request=request).deserialize(dict(request.POST))}
        )

    return _request_validator


def get_validation_schema(section: str) -> Any:
    """Метод соответствия раздела и схемы валидации"""
    schema = {
        "post_boarding_pass": BoardingPassPostValidator,
        "put_boarding_pass": BoardingPassPutValidator,
    }
    if section not in schema:
        raise KeyError(
            'Не найдена схема валидации фильтров для раздела "{}"'.format(section)
        )

    return schema[section]


# ----------------------------------- Схемы валидации фильтров запросов данных ----------------------------------


class BoardingPassPostValidator(MappingSchema):
    ticket_no = SchemaNode(String(), validator=Length(13))
    boarding_no = SchemaNode(Integer())
    seat_no = SchemaNode(String(), validator=Length(max=4))


class BoardingPassPutValidator(MappingSchema):
    seat_no = SchemaNode(String(), missing=drop, validator=Length(max=4))
