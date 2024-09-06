from typing import Any, Callable

from colander import (Float, Integer, Length, Mapping, MappingSchema,
                      SchemaNode, String, drop, Tuple, null, Invalid, SchemaType)
from study_proj.exceptions.exception_collection import ValidationFailure
import json

def id_validator(request, **kwargs):
    id_str = request.matchdict["airport_code"]
    if len(id_str) != 3:
        error_msg = "{} должно быть строкой длины 3".format(id_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="airport_code", message=error_msg)
    if id_str != id_str.upper():
        error_msg = "{} должен состоять из заглавных букв".format(id_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="airport_code", message=error_msg)
    try:
        request.validated["airport_code"] = id_str
    except ValueError:
        error_msg = "{} должно быть строкой формата XXX".format(id_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="airport_code", message=error_msg)


# ----------------------------------- Схемы валидации фильтров запросов данных ----------------------------------

class JsonType(SchemaType):
    def deserialize(self, node, cstruct):
        if not cstruct:
            return null
        try:
            result = json.loads(cstruct)
        except Exception as e:
            raise Invalid(node, "Not json")
        return result

def parse_tuple(string):
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        return
    except:
        return

class CoordType(SchemaType):
    def deserialize(self, node, cstruct):
        if not cstruct: #or type(cstruct) is not tuple:
            return null
        try:
            result = parse_tuple(cstruct)
        except Exception as e:
            raise Invalid(node, "Not coordinates")
        if type(result) is not tuple:
            raise Invalid(node, "Not coordinates")
        return result



class AirportsPostValidator(MappingSchema):
    airport_code = SchemaNode(
        String(), validator=Length(3, 3), alias="airport_code"
    )
    airport_name = SchemaNode(JsonType(), alias="airport_name")
    city = SchemaNode(JsonType(), alias="city")
    coordinates = SchemaNode(CoordType(), alias="coordinates")
    timezone = SchemaNode(String(), alias="timezone")


class AirportsPutValidator(MappingSchema):
    airport_name = SchemaNode(JsonType(), missing=drop, alias="airport_name")
    city = SchemaNode(JsonType(), missing=drop, alias="city")
    coordinates = SchemaNode(CoordType(), missing=drop, alias="coordinates")
    timezone = SchemaNode(String(), missing=drop, alias="timezone")
