"""init.py"""
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile("../config.py")


api = Api(app)
db = SQLAlchemy(app)

from app.Authentication import views
from app.Reviews import views
from app.Business import views
