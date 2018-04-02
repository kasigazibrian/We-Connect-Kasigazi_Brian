from flask import Flask
from flask_restplus import Api


app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

api = Api(app, description="WeConnect provides a platform that brings businesses and individuals together."
                           "This platform creates awareness for businesses and gives the users the ability "
                           "to write reviews about the businesses they have interacted with."
                           " Below is the documentation for the WeConnect RESTFUL API built using flask-restplus")

from app.v1.Authentication import views
from app.v1.Business import views
from app.v1.Reviews import views