from pyramid.paster import get_app, setup_logging
ini_path = '/study/development.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')
