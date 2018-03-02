"""Config.py"""

# Enable debugging
DEBUG = True

# Database URI
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:brian@localhost/tests'


SQLALCHEMY_TRACK_MODIFICATIONS = True

# secret key
SECRET_KEY = 'abcdefg'
