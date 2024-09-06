# coding: utf-8
# Collection of exceptions
import colander
from pyramid.view import exception_view_config, notfound_view_config
from sqlalchemy.exc import DataError, IntegrityError

from study_proj.exceptions.exception_collection import *
from study_proj.exceptions.controllers.exceptions import exception_response, create_trace

EXCEPTION_MESSAGE_LIST = {
    KeyError: {
        'msg': u"Отсутсвует данные с ключом: "
    },
    TypeError: {
        'msg': u"Ошибка типа данных: "
    },
    ValueError: {
        'msg': u"Ошибка значения: "
    },
    DataError: {
        'msg': u"Ошибка базы данных: "
    },
    IntegrityError: {
        'msg': u"Ошибка целосности данных: "
    },
    Exception: {
        'msg': 'Общая ошибка: '
    },
    NameTypeError: {
        'msg': 'Запрошены несуществуюшие состояния у объекта: '
    }
}


# # Validation error
# def valid_error(request):
#     errors = request.errors
#     message_er = 'Валидация: Не заполнены обязательные поля '
#     # Print problems in console
#     for error in errors:
#         logging.error(str(error))
#     return exception_response(
#         trace_dict=create_trace(),
#         special=request,
#         msg=message_er
#     )


@exception_view_config(Exception, renderer='json')
def external_error(request):
    for exception in EXCEPTION_MESSAGE_LIST.keys():
        if isinstance(request.exception, exception):
            msg = EXCEPTION_MESSAGE_LIST[exception]['msg']
            return exception_response(
                msg=msg,
                trace_dict=create_trace()
            )
    return exception_response(
        trace_dict=create_trace()
    )


# #########################################USER ERRORS####################################
@exception_view_config(LogicException, renderer='json')
def error_logic(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка ведения информационного объета. Проверте введеные данные '
    )


@exception_view_config(ConfigError, renderer='json')
def config_error(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка прочтения конфигурационного файла '
    )


@exception_view_config(RuntimeException, renderer='json')
def error_logic(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка исполнения '
    )


@exception_view_config(colander.Invalid, renderer='json')
def error_validation(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка валидации или не заполнены обязательные поля '
    )


@exception_view_config(ValidationFailure, renderer='json')
def user_error_validation(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Валидация формы '
    )


@exception_view_config(DisplayFailure, renderer='json')
def error_display(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Невозможно отобразить запрашиваемые данные '
    )


@exception_view_config(DbError, renderer='json')
def error_db(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка базы данных.'
    )


@exception_view_config(ReportError, renderer='json')
def error_report(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка формирования отчета или документа отчета '
    )


@exception_view_config(FormationError, renderer='json')
def error_formation(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка формирования ответа сервера информации '
    )


@exception_view_config(FilterError, renderer='json')
def error_filter(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка фильтров. Подставлен неправильный фильтр '
    )


@exception_view_config(SendException, renderer='json')
def error_filter(request):
    return exception_response(
        special=request,
        trace_dict=create_trace(),
        msg='Ошибка отправки изменений  '
    )


@notfound_view_config(request_method='GET')
def notfound_view(request):
    return exception_response(
        msg='Не найдена страница (GET - 404)',
        special=request
    )


@notfound_view_config(request_method='POST')
def notfound_view(request):
    return exception_response(
        msg='Не найдена страница (POST - 404)',
        special=request
    )
