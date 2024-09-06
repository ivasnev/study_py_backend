# coding: utf-8
from pyramid.config import Configurator
from study_proj.sysfuncs.session_maker import session_maker
from cornice_swagger import cornice_enable_openapi_explorer


def db(request):
    session = session_maker(request)
    return session


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.add_request_method(db, reify=True)
    config.include('pyramid_chameleon')
    config.include('cornice')
    config.include('cornice_swagger')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
