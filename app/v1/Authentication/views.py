"""views.py"""
from flask import request, jsonify, make_response
from app.v1 import app, api
from flask_restful import Resource
from app.v1.Authentication.models import User
from functools import wraps
import jwt


def jwt_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if token:
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'])
                    current_user = data['username']
                except:
                    return jsonify({'message': 'Token is missing'})
            else:
                return jsonify({'message': 'Token is missing'})
        else:
            return jsonify({'message': 'Token is missing'})
        return f(current_user, *args, **kwargs)
    return decorated


class Home(Resource):
    """Class for the home page"""
    def get(self):
        return {'message': 'Success'}


class Register(Resource):
    """Class for registering a user """
    def post(self):
        test_user = request.get_json(force=True)
        user_id = test_user.get('user_id')
        username = test_user.get('username')
        password = test_user.get('password')
        first_name = test_user.get('first_name')
        last_name = test_user.get('last_name')
        email = test_user.get('email')
        gender = test_user.get('gender')
        new_user = User(user_id=user_id, username=username, password=password, first_name=first_name,
                        last_name=last_name,
                        email=email, gender=gender)
        response = User.register(new_user)
        return response


class Login(Resource):
    """Class for logging in a user"""
    def post(self):
        """obtain user data sent in a post request"""
        test_user = request.get_json(force=True)
        username = test_user.get('username')
        password = test_user.get('password')
        res = User.login(username=username, password=password)
        res.status_code = 201
        return res


class Logout(Resource):
    """class for logging out a user"""
    @jwt_required
    def post(self, current_user):
        # obtain user data sent in a post request
        if current_user:
            user_data = request.get_json(force=True)
            user_id = user_data.get('user_id')
            logout_res = User.logout(user_id=user_id)
            return logout_res


class ResetPassword(Resource):
    """class for resetting user password"""
    @jwt_required
    def post(self, current_user):
        if current_user:
            new_password = request.get_json(force=True)
            my_new_password = new_password.get('password')
            if my_new_password:
                response = User.password_reset(new_password=new_password)
                # Call on the password_reset method
                response.status_code = 200
                return response
            else:
                return jsonify({'message': 'Failed to update password'})
        else:
            # return jsonify({'message': 'Please log in to access this page'})
            return str(current_user.moses)


api.add_resource(Home, '/')
api.add_resource(Register,'/api/v1/auth/register')
api.add_resource(Login,'/api/v1/login')
api.add_resource(Logout,'/api/v1/auth/logout')
api.add_resource(ResetPassword,'/api/v1/auth/reset-password')