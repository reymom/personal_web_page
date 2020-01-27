import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    POSTGRES = {
        'user': 'reymon',
        'pw': 'reymon',
        'db': 'dbweb',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

    SQLALCHEMY_TRACK_MODIFICATIONS = False
