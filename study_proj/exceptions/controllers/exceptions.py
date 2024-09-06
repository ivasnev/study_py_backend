# coding=utf-8

import logging
import sys
import traceback

import transaction
from pyramid.threadlocal import get_current_request
from study_proj.exceptions.template import BaseHhtpException
from study_proj.exceptions.exception_collection import AppException
from colander import Invalid


def create_trace():
    exc_type, exc_value, exc_traceback = sys.exc_info()

    request = get_current_request()
    # Print Error in log + console
    # Prepare log
    logger = logging.getLogger(__name__)
    for string in traceback.format_exception(exc_type, exc_value, exc_traceback):
        logger.error(msg=string)

    logger.error(msg=prepare_information(request.environ))

    # Print json-body if request method == post
    if request.environ.get('REQUEST_METHOD', None) == 'POST':
        logger.error(
            request.body
        )

    # Information for json
    trace = {
        'trace': traceback.format_tb(exc_traceback),
        'exc_value': exc_value
    }
    # Close transaction
    transaction.abort()

    return trace


# Transformation  environ to text information
def prepare_information(environ_dict):
    string_env = dict()
    for key in environ_dict.keys():
        if isinstance(environ_dict[key], str):
            string_env[key] = environ_dict[key]
    return string_env


def error(**kwargs):
    if 'trace_dict' in kwargs.keys():
        if kwargs['trace_dict'] is not None:
            exc_value = kwargs['trace_dict']['exc_value']
            if exc_value is not None:
                if issubclass(exc_value.__class__, AppException):
                    return exc_value.message
                if isinstance(exc_value, Invalid):
                    return("colander.Invalid: " + ",".join(["%s %s" % (k, v) for k,v in exc_value.asdict().items()]))
                return kwargs['msg'] + str(exc_value)

    return kwargs['msg']


def exception_response(**kwargs):
    """
        Args:
             msg (str): сообщение о ошибке
             error_msg (str): номер ошибки
             field_name&number_string  (str/int): Имя поля/номер строки

        **Ответ сервера**:


        .. sourcecode:: javascript


            {
                'status': Статус сообщения,
                'error': Текстовое сообщение о ошибке,
                'fieldname': Имя поля/номер строки,
                'service': {
                    'method': Каким методом был выполнен запрос,
                    'url': По какому урлу,
                    'parameters': С какими параметрами,
                },
                'wsgi': Вся остальная информация от окружения WSGI
            }


        :returns: Готовый сформированный отчет о ошибке
        :rtype: json

    """

    # афтар, убей себя об стену! вот никуя не ясно почему-откуда берутся поля

    # traceback.print_exc()
    response = BaseHhtpException()
    # For js
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.content_type = "application/json"
    # Information from WSGI
    if 'special' in kwargs.keys():
        request = kwargs['special']
        environ = request.environ
        # response.code = request.code
    else:
        environ = get_current_request().environ
    # Body report
    error_ = error(**kwargs)
    error_correct = error_ if error_ is not None else "Сервер не смог обработать запрос пользователя."
    body_json = {
        'status': '',
        # Message for user
        'error': 'Вид ошибки: ' + error_correct,
        'service': {
            'method': environ.get('REQUEST_METHOD', ''),
            'url': environ.get('PATH_INFO', ''),
            'parameters': environ.get('QUERY_STRING', ''),
        },
        'wsgi': prepare_information(environ)
    }

    if 'special' in kwargs.keys():
        # Treatment exception message
        exception = kwargs['special'].exception
        # если исключение не подкласс AppException, у него не будет полей fieldname и message
        if exception and issubclass(exception.__class__, AppException):
            body_json['fieldname'] = exception.fieldname
            # If error have message for GUI
            exception_message = exception.message
            if exception_message != '' and not exception_message in body_json['error']:
                body_json['error'] += '. ' + exception_message
            else:
                # Add information in service fields
                exc_field = kwargs['trace_dict']['exc_value']
                body_json['validation_error'] = str(exc_field) \
                        if exc_field is not None \
                        else 'Нет информации о полях  в которых произошла ошибка'
                # # Validation error have 400 status
                # if response.code != 400:
                #     body_json['error'] += '. Ошибка вызвана открытием несуществующего ресурса.'

    # Add trace log if is exist
    if kwargs.get('trace_dict', None) is not None:
        if kwargs['trace_dict'].get('trace', None) is not None:
            body_json['trace'] = kwargs['trace_dict']['trace']

    # Add json in response
    response.json = body_json
    return response

