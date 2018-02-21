"""views.py"""

from flask import request, jsonify
from app import app
from app.models import Signup



@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    return "success"


@app.route('/api/auth/register', methods=['POST'])
# creates user account
def register():
    if request.method == 'POST':
        test_user = request.get_json()
        id = test_user['id']
        username = test_user['username']
        password = test_user['password']
        firstname =test_user['firstname']
        lastname = test_user['lastname']
        email = test_user['email']
        gender = test_user['gender']

        if id and username and password and firstname and lastname and email and gender:
            new_user = Signup(id=id, username=username, password=password, firstname=firstname, lastname=lastname,
                              email=email, gender=gender)
            response = jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'password': new_user.password,
                'firstname': new_user.firstname,
                'lastname': new_user.lastname,
                'gender': new_user.gender,
                'email': new_user.email
            })
            return response
        else:
            return 'fail'

@app.route('/api/v1/auth/login', methods=['POST'])
# Logs in a user
def login():
    if request.method == 'GET':
        user = {
            'id':'1',
            'username':'Mary',
            'password':'mango',
        }
        return jsonify(user)

@app.route('/api/auth/logout', methods=['GET', 'POST'])
# Logs out a user
def logout():
    pass


@app.route('/api/auth/reset-password', methods=['POST'])
# reset user password
def reset_password():
   if request.method=='POST':
       newpassword ={'password':'apple'}
       return jsonify(newpassword)


@app.route('/api/businesses', methods=['POST'])
#  Register a business
def businesses():
    newbusiness = {
        'id':'1',
        'businessname':'supercom',
        'businesslocategory':'entertainment',
        'businesslocation':'kampala',
        'email':'supercom@gmail.com',
        'contactnumber':'256781712929'
    }
    return jsonify(newbusiness)


@app.route('/api/businesses/<business_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# view specific business
def specific_business(business_id):
    if request.method == 'GET':
        business = request.get_json()
        id = business['id']
        businesname = business['business']
        businesslocation = business['businesslocation']
        businesscategory = business['businesscategory']
        email = business['email']
        contactnumber =['contactnumber']
        if id and businesscategory and businesslocation and businesscategory and businesname and email:
            new_user = Signup(id=id, businesname=businesname, businesslocation=businesslocation, email=email, contactnumber=contactnumber)
            response = jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'password': new_user.password,
                'firstname': new_user.firstname,
                'lastname': new_user.lastname,
                'gender': new_user.gender,
                'email': new_user.email
            })
            return response
        else:
            return 'fail'

    if request.method=='POST':
        pass
    if request.method=='DELETE':
        pass
    if request.method=='PUT':
        pass

@app.route('/api/businesses/<business_id>/reviews', methods=['GET', 'POST'])
def reviews():
    pass