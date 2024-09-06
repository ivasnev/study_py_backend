# -*- coding: utf-8 -*-
import json
from typing import Any, Callable

import colander
from colander import (Float, Integer, Invalid, Length, Mapping, MappingSchema,
                      Range, SchemaNode, String, drop)

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


def id_validator(request, **kwargs):
    id_str = request.matchdict["aircraft_code"]
    if len(id_str) != 3:
        error_msg = "%s должно быть строкой длины 3" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="aircraft_code", message=error_msg)
    if id_str != id_str.upper():
        error_msg = "%s должен состоять из заглавных букв" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="aircraft_code", message=error_msg)
    try:
        request.validated["aircraft_code"] = id_str
    except ValueError:
        error_msg = "%s должно быть строкой формата <XXX>" % id_str
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="aircraft_code", message=error_msg)


def get_validation_schema(section: str) -> Any:
    """Метод соответствия раздела и схемы валидации"""
    schema = {
        "post_aircraft": AircraftsPostValidator,
        "put_aircraft": AircraftsPutValidator,
    }
    if section not in schema:
        raise KeyError(
            'Не найдена схема валидации фильтров для раздела "{}"'.format(section)
        )

    return schema[section]


def values_are_singularly_typed_dicts(node, mapping):
    for val in mapping.values():
        if not isinstance(val, dict):
            raise colander.Invalid(
                node, "%r one or more value(s) is not a dict" % mapping
            )


# ----------------------------------- Схемы валидации фильтров запросов данных ----------------------------------


class JsonType(colander.SchemaType):
    def deserialize(self, node, cstruct):
        if not cstruct:
            return colander.null
        try:
            result = json.loads(cstruct)
        except Exception as e:
            raise Invalid(node, "Not json")
        return result


class AircraftsPostValidator(MappingSchema):
    aircraft_code = SchemaNode(String(), validator=Length(3), alias="aircraft_code")
    model = SchemaNode(JsonType())
    range = SchemaNode(Integer(), validator=Range(500, 30000), alias="range")


class AircraftsPutValidator(MappingSchema):
    model = SchemaNode(JsonType(), missing=drop, alias="model")
    range = SchemaNode(Integer(), missing=drop, alias="range")


# def model_validator(node, value):
#     try:
#         json.loads(value)
#     except json.JSONDecodeError:
#         raise Invalid(node,
#                       '%r is not a aircraft model' % value)
