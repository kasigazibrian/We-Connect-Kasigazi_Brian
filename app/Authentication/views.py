from flask import request, jsonify
from flask_restful import Resource
from app import app, api
from werkzeug.security import generate_password_hash
from app.models import User, Token
import jwt
from functools import wraps


def jwt_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            if token:
                if Token.check_blacklisted_token(token=token) is False:
                    try:
                        data = jwt.decode(token, app.config['SECRET_KEY'])
                        current_user = User.query.filter_by(username=data['username']).first()

                    except:
                        return jsonify({'message': 'Token is missing'})
                else:
                    return jsonify({"message":"Your session has expired!. Please login to perform action"})
            else:
                return jsonify({'message': 'Token is missing'})
        else:
            return jsonify({'message': 'Token is missing'})
        return f(current_user, *args, **kwargs)
    return decorated


class Home(Resource):
    def get(self):
        """route to home page"""
        return jsonify({'message':'You are Welcome!'})


class Register(Resource):
    """class for register"""
    def post(self):
        """Method to register a user"""
        new_user = request.get_json(force=True)
        username = new_user.get('username')
        password = new_user.get('password')
        first_name = new_user.get('first_name')
        last_name = new_user.get('last_name')
        email = new_user.get('email')
        gender = new_user.get('gender')
        if username and password and first_name and last_name and email and gender:
            hashed_password = generate_password_hash(password, method='sha256')
            if not User.query.filter_by(username=username).first():
                if not User.query.filter_by(email=email).first():
                    login_status = False
                    add_new_user = User(username=username, password=hashed_password, first_name=first_name,
                                    last_name=last_name, email=email, gender=gender, login_status=login_status)

                    response = User.add_user(add_new_user)
                    return  response
                else:
                    return jsonify({"message":"Email address already exists"})
            else:
                return jsonify({'message':'User already exists'})
        else:
            return jsonify({'message': 'All fields are required'})


class Login(Resource):
    def post(self):
        """Logs in a user"""
        test_user = request.get_json()
        username = test_user.get('username')
        password = test_user.get('password')
        if username and password:
            response = User.login(username=username,password=password)
            return response

        else:
            return jsonify({"message": "Both username and password are required"})


@app.route('/api/v2/auth/logout', methods=['POST'])
@jwt_required
def logout(current_user):
    if current_user.login_status is True:
        if 'access-token' in request.headers:
            token = request.headers['access-token']
            response = Token.blacklist_token(token=token,user=current_user.username)
            return response
        else:
            return jsonify({"message":"Token is missing"})
    else:
        return jsonify({"message":"Please first login to perform the action"})




class PasswordReset(Resource):
    """class for resetting password"""
    # @jwt_required
    def post(self, current_user):
        """Reset user password"""
        new_user_data = request.get_json(force=True)
        new_password = new_user_data.get('password')
        response = User.password_reset(current_user, new_password)
        return response

api.add_resource(Home, '/')
api.add_resource(Register, '/api/v2/auth/register')
api.add_resource(Login, '/api/v2/login')
api.add_resource(PasswordReset, '/api/v2/auth/reset-password')