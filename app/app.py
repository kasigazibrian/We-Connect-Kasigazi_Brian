from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
api = Api(app)


