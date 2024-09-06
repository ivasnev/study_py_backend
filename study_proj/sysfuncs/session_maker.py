# coding: utf-8
import os

from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base

try:
    from ALDUtils import ald
except:
    print('Error : Lib ALDUtils not imported')

Base = declarative_base()


def session_returner(request, connect_line):
    debug = bool(int(request.registry.settings['debug']))  # получаем флаг на вывод генерируемых запросов sql
    engine = create_engine(connect_line, echo=debug)
    Base.metadata.bind = engine
    Session = orm.sessionmaker(bind=engine, autoflush=False)
    session = Session()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        #        else:
        #            try:
        #                session.commit()
        #            except exc.InvalidRequestError:
        #                print('Error : No transaction is begun. session.commit() - pass')
        #                pass
        session.close()

    request.add_finished_callback(cleanup)

    return session


def get_settings(request):
    request.response.headers["Access-Control-Allow-Origin"] = "*"
    settings = request.registry.settings
    return settings


def kerber_finder(request, settings):
    if bool(int(settings['enter_with_keber'])):
        if 'KRB5CCNAME' in request.environ.keys():
            return True
        else:
            print('Error : No KRB5CCNAME in environ')
    else:
        return False


def get_user_dict(request):
    settings = get_settings(request)
    remote_user = get_user_name(request)
    if kerber_finder(request, settings):
        ald_info = ald.get_user_info(remote_user)
        return {
            u'description': ald_info['Description'],
            u'name': ald_info['FullUserName']
        }
    else:
        return {
            u'name': remote_user,
            u'description': None
        }


def get_user_name(request, settings=False):
    if not settings:
        settings = get_settings(request)
    if kerber_finder(request, settings):
        remote_user = request.environ['REMOTE_USER'].split('@')[0]
        os.environ['KRB5CCNAME'] = request.environ['KRB5CCNAME']
        return remote_user
    else:
        return 'www-data'


def get_user_fullname(request):
    settings = get_settings(request)
    remote_user = get_user_name(request)
    if kerber_finder(request, settings):
        ald_info = ald.get_user_info(remote_user)
        return ald_info['Description'] + ' ' + ald_info['FullUserName']
    else:
        session = session_maker(request)
        fname = session.query(Dsysuser.fnamesysusers).filter(Dsysuser.namesysusers == remote_user).first()[0]
        return fname


def session_maker(request, settings=None):
    # Choose settings
    if settings is None:
        settings = get_settings(request)

    if kerber_finder(request, settings):
        remote_user = get_user_name(request, settings)
        connect_line = 'postgresql://{user}@{postgre_server}:{bd_port}/{bd_name}' \
            .format(user=remote_user,
                    postgre_server=settings['postgre_server'],
                    bd_port=settings['bd_port'],
                    bd_name=settings['bd_name'])

        return session_returner(request, connect_line)
    else:
        connect_line = 'postgresql://{user}:{password}@{postgre_server}:{bd_port}/{bd_name}' \
            .format(user=settings['bd_user'],
                    postgre_server=settings['postgre_server'],
                    bd_port=settings['bd_port'],
                    password=settings['bd_password'],
                    bd_name=settings['bd_name'])

        return session_returner(request, connect_line)
