# -*- coding: utf-8 -*-
import json
from typing import Any, Callable

import colander
from colander import (Invalid, Length, MappingSchema,
                      SchemaNode, String, drop)

from study_proj.exceptions.exception_collection import ValidationFailure


# ----------------------------------------------- Общие методы валидации -----------------------------------------------


def request_validator(section: str) -> Callable:
    """Метод валидации параметров запроса"""
    schema = get_validation_schema(section)

    def _request_validator(request, **kwargs) -> None:
        request.validated.update(
            {"filters": schema().bind(request=request).deserialize(dict(request.POST))}
        )

    return _request_validator


def ticket_no_validator(request, **kwargs):
    id_str = request.matchdict["ticket_no"]
    if len(id_str) != 13:
        error_msg = "%s должно быть строкой длины 13" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="ticket_no", message=error_msg)
    if id_str != id_str.upper():
        error_msg = "%s должен состоять из заглавных букв" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="ticket_no", message=error_msg)
    try:
        request.validated["ticket_no"] = id_str
    except ValueError:
        error_msg = "%s должно быть строкой из заглавных букв длины 13" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="ticket_no", message=error_msg)


def get_validation_schema(section: str) -> Any:
    """Метод соответствия раздела и схемы валидации"""
    schema = {
        "post_ticket": TicketsPostValidator,
        "put_ticket": TicketsPutValidator,
    }
    if section not in schema:
        raise KeyError(
            'Не найдена схема валидации фильтров для раздела "{}"'.format(section)
        )

    return schema[section]


# ----------------------------------- Схемы валидации фильтров запросов данных ----------------------------------


class JsonType(colander.SchemaType):
    @staticmethod
    def deserialize(node, cstruct):
        if not cstruct:
            return colander.null
        try:
            result = json.loads(cstruct)
        except Exception as e:
            raise Invalid(node, "Not json")
        return result


class TicketsPostValidator(MappingSchema):
    ticket_no = SchemaNode(String(), validator=ticket_no_validator)
    book_ref = SchemaNode(String(), validator=Length(6))
    passenger_id = SchemaNode(String(), validator=Length(20))
    passenger_name = SchemaNode(String())
    contact_data = SchemaNode(JsonType(), missing=drop)


class TicketsPutValidator(MappingSchema):
    book_ref = SchemaNode(String(), missing=drop, validator=Length(6))
    passenger_id = SchemaNode(String(), missing=drop, validator=Length(20))
    passenger_name = SchemaNode(String(), missing=drop)
    contact_data = SchemaNode(JsonType(), missing=drop)

