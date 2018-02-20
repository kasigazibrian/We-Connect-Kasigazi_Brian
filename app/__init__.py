from flask import Flask, jsonify, request

import os
app = Flask(__name__)

app.config.from_pyfile('../config.py')


from app import views

