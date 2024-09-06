from typing import Any, Callable

from colander import (Float, Integer, Length, Mapping, MappingSchema,
                      SchemaNode, String, drop, Tuple, null, Invalid, SchemaType, OneOf)
from study_proj.exceptions.exception_collection import ValidationFailure
import json


def id_validator(request, **kwargs):
    code_str = request.matchdict["aircraft_code"]
    if len(code_str) != 3:
        error_msg = "{} должно быть строкой длины 3".format(code_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="aircraft_code", message=error_msg)
    try:
        request.validated["aircraft_code"] = code_str
    except ValueError:
        error_msg = "{} должно быть строкой формата XXX".format(code_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="aircraft_code", message=error_msg)

    seat_str = request.matchdict["seat_no"]
    if len(seat_str) > 4:
        error_msg = "{} должно быть строкой длины 4 или меньше".format(seat_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="seat_no", message=error_msg)
    try:
        request.validated["seat_no"] = seat_str
    except ValueError:
        error_msg = "{} должно быть строкой формата ????".format(seat_str)
        request.errors.append(error_msg)
        raise ValidationFailure(fieldname="seat_no", message=error_msg)


# ----------------------------------- Схемы валидации фильтров запросов данных ----------------------------------


class SeatsPostValidator(MappingSchema):
    aircraft_code = SchemaNode(
        String(), validator=Length(3, 3), alias="aircraft_code"
    )
    seat_no = SchemaNode(String(), validator=Length(1, 4), alias="seat_no")
    fare_conditions = SchemaNode(String(), validator=OneOf(['Economy', 'Comfort', 'Business']), alias="fare_conditions")


class SeatsPutValidator(MappingSchema):
    fare_conditions = SchemaNode(String(), validator=OneOf(['Economy', 'Comfort', 'Business']), missing=drop, alias="fare_conditions")
