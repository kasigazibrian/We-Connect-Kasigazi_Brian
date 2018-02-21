from flask import jsonify
from flask_jwt import JWT, jwt_required, current_identity

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    # def __str__(self):
    #     return "User(id='%s')" % self.id
#users=[User(1,'brian','abcd'),User(2,'Dan','abcdef')]


class Business(object):
    def __init__(self, id, businessname, businesslocation, businesscategory, contactnumber, email):
        self.id= id
        self.businessname= businessname
        self.businesslocation = businesslocation
        self.businesscategory = businesscategory
        self.contactnumber = contactnumber
        self.email = email

    def __str__(self):
        return "Business(id='%s')" % self.id

class Signup(object):
    def __init__(self,id,firstname, lastname, username, password,email, gender):
        self.id = id
        self.firstname = firstname
        self.lastname=lastname
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
    def __str__(self):
        return "Signup(id='%s')" % self.id
class Reviews(object):
    def __init__(self, id, review):
        self.id = id
        self.review = review

    def __str__(self):
        return "Reviews(id='%s')" % self.id
