from flask import jsonify
from flask_jwt import JWT, jwt_required, current_identity

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'brian', 'abcd'),
    User(2, 'gita', 'abcdef'),
]

class business(object):
    def __init__(self, id, businessname, businesslocation, businesscategory, contactnumber, email):
        self.id= id
        self.businessname= businessname
        self.businesslocation = businesslocation
        self.businesscategory = businesscategory
        self.contactnumber = contactnumber
        self.email = email

    def __str__(self):
        return "User(id='%s')" % self.id
