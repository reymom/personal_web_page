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

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['ramonfcb@hotmail.com', 'ramon_gs95@hotmail.com']

    PREDICTIONS_PER_PAGE_USER = 10
    PREDICTIONS_PER_PAGE_INDEX = 3

    LANGUAGES = ['en', 'es', 'ca', 'de']
