import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'confweb.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 's3cr3t'
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
            os.environ.get('DB_USER'), os.environ.get('DB_PSSW'), os.environ.get('DB_HOST'),
            os.environ.get('DB_PORT'), os.environ.get('DB_NAME'))
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

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')