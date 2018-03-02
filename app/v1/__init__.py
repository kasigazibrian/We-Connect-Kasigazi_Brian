from flask import Flask
from flask_restful import Api


app = Flask(__name__)

app.config.from_pyfile("../../config.py")

api = Api(app)

from app.v1.Authentication import views
from app.v1.Business import views
from app.v1.Reviews import views