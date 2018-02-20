#import everything from app
from app import *
from app.models import User

@app.route('/')
@app.route('/home', methods=['GET','POST'])
def home():
    return "success"

#creates user account
@app.route('api/auth/register', methods=['GET','POST'])
def register():
    pass



#Logs in a user
@app.route('api/auth/login', methods=['GET','POST'])
def login():
    if request.method=='GET':
        response = jsonify({})
        response.status_code = 200
        return response

    elif request.method == 'POST':
        newuser = User(username=str(request.data.get('username')),
                       password=str(request.data.get('password')))
        response = jsonify({'username': newuser.username, 'password': newuser.password})
        response.status_code = 200
        return response

# Logs out a user
@app.route('api/auth/logout', methods=['GET','POST'])
def logout():
    pass

# reset user password
@app.route('api/auth/reset-password', methods=['GET','POST'])
def resetpassword():
   pass

#  Register a business
@app.route('api/businesses', methods=['GET','POST'])
def businesses():
    pass

#view specific business
@app.route('api/businesses/<businessid>', methods=['GET','POST'])
def specificbusiness(businessid):
    pass

# Updates a business profile
@app.route('update/api/businesses/<businessid>', methods=['PUT'])
def updatebusiness(businessid):
    pass

# delete a business profile
@app.route('/delete/api/businesses/<businessid>', methods=['DELETE'])
def deletebusiness(businessid):
    pass