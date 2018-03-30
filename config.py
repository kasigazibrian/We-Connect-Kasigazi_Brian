"""Config.py"""


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'abcdefg'


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    # Enable debugging
    DEBUG = True

class TestingConfig(Config):
    # Enable testing
    TESTING = True
    DEBUG = True



