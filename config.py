"""Config.py"""
import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'abcdefg'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SWAGGER_UI_JSONEDITOR = True
    # Database URI
    if "DATABASE_URL" in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:brian@localhost/weconnect'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    # Enable testing
    TESTING = True

    #Tests URI
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:brian@localhost/tests'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
