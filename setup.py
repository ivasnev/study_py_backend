# coding: utf-8
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'cornice',
    'colander',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'psycopg2-binary',
    'geoalchemy2',
    'pyparsing',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
]

docgen_require = [
    'Sphinx >= 2.0.1',
    'sphinxcontrib-confluencebuilder',
]

setup(name='study_proj',
      version='0.0',
      description='study_proj',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
          'doc': docgen_require
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = study_proj:main
      
      """,
      )
