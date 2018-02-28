from flask import Flask
from flask_restful import Api


app = Flask(__name__)

app.config.from_pyfile("../config.py")

api = Api(app)

from app.Authentication import views
from app.Reviews import views
from app.Business import views