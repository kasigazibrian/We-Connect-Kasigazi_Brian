"""views.py"""
from flask import request, jsonify, make_response
from app.v1 import app, api
from flask_restplus import Resource, fields
from app.v1.Authentication.models import User
from functools import wraps
import jwt


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            if token:
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'])
                    current_user = data['username']
                except jwt.ExpiredSignatureError:
                    return jsonify({'message': 'Your session has expired, Please login again'})
            else:
                return jsonify({'message': 'Token is missing'})
        else:
            return {'message': 'Token is missing'}
        return f( *args, current_user, **kwargs)
    return decorated


registered_users = []

authorizations = {'api_key':{
    'type': 'apiKey',
    'in': 'header',
    'name': 'access-token'

}}
User_model = api.model('User',
                        {'first_name': fields.String('First Name', required=True),
                            'last_name': fields.String('Last Name', required=True),
                            'username': fields.String('Username', required=True),
                            'email': fields.String('Email', required=True),
                            'gender': fields.String('Gender', required=True),
                            'password': fields.String('Password', required=True)
                        }
                       )
login_model = api.model('Login', {'username': fields.String('Username', required=True),
                                  'password': fields.String('Password', required=True)
                                 }
                        )
new_password_model = api.model('Reset_password', {'new_password': fields.String('New password')})

api.authorizations = authorizations


@api.route('/home')
class Home(Resource):
    """Class for the home page"""
    def get(self):
        """Route to home page"""
        return {'message': 'You are welcome'}, 200


@api.route('/api/v1/auth/register')
class Register(Resource):
    """Class for registering a user """
    @api.expect(User_model)
    def post(self):
        """Method for registering a new user"""
        test_user = api.payload
        if "username" in test_user:
            username = test_user['username']
        else:
            return {"message": "Username is missing"}
        if "password" in test_user:
            password = test_user['password']
        else:
            return {"message": "password is missing"}
        if "first_name" in test_user:
            first_name = test_user['first_name']
        else:
            return {"message": "first_name is missing"}
        if "last_name" in test_user:
            last_name = test_user['last_name']
        else:
            return {"message": "last_name is missing"}
        if "email" in test_user:
            email = test_user['email']
        else:
            return {"message": "email is missing"}
        if "gender" in test_user:
            gender = test_user['gender']
        else:
            return {"message": "gender is missing"}
        test_user['user_id'] = len(registered_users) + 1
        user_id = test_user['user_id']
        user_availability = [user for user in registered_users if user['username'] == username]
        email_availability = [user for user in registered_users if user['email'] == email]
        if username and password and first_name and last_name and email and gender:
            if not user_availability:
                if not email_availability:
                    if User.is_valid_email(email=email) is True:
                        if User.is_valid_gender(gender=gender) is True:
                            new_user = User(user_id=user_id, username=username, password=password, first_name=first_name,
                                            last_name=last_name,
                                            email=email, gender=gender, login_status=False)
                            response = User.register(new_user)
                            registered_users.append(response)
                            return {"message": "User "+first_name+" "+last_name+" has been registered successfully"}, 201
                        else:
                            return {'message': 'Invalid gender, Try Female, Male, F, M'}, 200
                    else:
                        return {'message': 'Invalid email address'}, 200
                else:
                    return {'message': 'Email already exists'}, 200
            else:
                return {'message': 'User already exists'}, 200
        else:
            return {'message': 'All fields are required'}, 200


@api.route('/api/v1/login')
class Login(Resource):
    """Class for logging in a user"""
    @api.expect(login_model)
    def post(self):
        """obtain user data sent in a post request and log in a user"""
        test_user = api.payload
        if 'username' in test_user:
            username = test_user['username']
        if 'password' in test_user:
            password = test_user['password']
        res = User.login(username=username, password=password, registered_users=registered_users)
        return res


@api.route('/api/v1/auth/logout')
class Logout(Resource):
    """class for logging out a user"""
    decorators = [jwt_required]

    @api.doc(security='api_key')
    def post(self, current_user):
        """Method for logging out a user"""
        logout_res = User.logout(current_user=current_user, registered_users=registered_users)
        return logout_res


@api.route('/api/v1/auth/reset-password')
class ResetPassword(Resource):
    """class for resetting user password"""
    decorators = [jwt_required]

    @api.doc(security='api_key')
    @api.expect(new_password_model)
    def post(self, current_user):
        """Method for resetting a users password"""
        new_password = api.payload
        if 'new_password' in new_password:
            my_new_password = new_password['new_password']
            response = User.password_reset(new_password=my_new_password, current_user=current_user,
                                           registered_users= registered_users)
            # Call on the password_reset method
            return response
        else:
            return {'message': 'Failed to update password, Please enter the new password'}