from flask import request, jsonify
from flask_restplus import Resource, fields
from app.app import app, api
from werkzeug.security import generate_password_hash
from app.models import User, Token, db
import jwt
from functools import wraps

authorizations = {'api_key':{
    'type': 'apiKey',
    'in': 'header',
    'name': 'access-token'

}}


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
                    except jwt.ExpiredSignatureError:
                        my_token = Token.query.filter_by(token=token).first()
                        my_token.tk_owner.login_status = False
                        my_token.blacklist = True
                        db.session.commit()
                        return {'message': 'Your session has expired!. Please log in again.'}, 401

                else:
                    return {"message":"Your session has expired!. Please login again"}, 401
            else:
                return {'message': 'Token is missing'}, 401
        else:
            return {'message': 'Token is missing'}, 401
        return f(*args, current_user, **kwargs)
    return decorated


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


class Home(Resource):
    def get(self):
        """route to home page"""
        return {'message':'You are Welcome!'}, 200


class Register(Resource):
    """class for registering a user"""
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created'})
    @api.expect(User_model)
    def post(self):
        """Method to register a user"""
        new_user = api.payload
        if 'username' in new_user:
            username = new_user['username']
        if 'password' in new_user:
            password = new_user['password']
        if 'first_name' in new_user:
            first_name = new_user['first_name']
        if 'last_name' in new_user:
            last_name = new_user['last_name']
        if 'email' in new_user:
            email = new_user['email']
        if 'gender' in new_user:
            gender = new_user['gender']
        if username and password and first_name and last_name and email and gender:
            if User.is_valid_email(email) is True:
                if User.is_valid_gender(gender) is True:
                    hashed_password = generate_password_hash(password, method='sha256')
                    if not User.query.filter_by(username=username).first():
                        if not User.query.filter_by(email=email).first():
                            login_status = False
                            add_new_user = User(username=username, password=hashed_password, first_name=first_name,
                                                last_name=last_name, email=email, gender=gender,
                                                login_status=login_status)

                            response = User.add_user(add_new_user)
                            return response
                        else:
                            return {"message": "Email address already exists"}, 400
                    else:
                        return {'message': 'User already exists'}, 400
                else:
                    return {'message': 'Invalid gender. Try Male, Female, M, F'}, 400
            else:
                return {"message": "Not a valid email address"}, 400
        else:
            return {'message': 'All fields are required, that is username,'
                               ' password, first_name, last_name, email and gender'}, 400


class Login(Resource):
    """Class for logging in a user"""
    @api.expect(login_model)
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created'})
    def post(self):
        """Logs in a user"""
        test_user = api.payload
        username = test_user.get('username')
        password = test_user.get('password')
        if username and password:
            response = User.login(username=username, password=password)
            return response
        else:
            return {"message": "Both username and password are required"}, 400


class PasswordReset(Resource):
    """Class for resetting a user password"""
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @jwt_required
    @api.expect(new_password_model)
    def post(self, current_user):
        """Reset user password post request"""
        new_user_data = api.payload
        if 'new_password' in new_user_data:
            new_password = new_user_data['new_password']
            if new_password:
                my_new_password = generate_password_hash(new_password, method='sha256')
                response = User.password_reset(current_user, my_new_password)
                return response
            else:
                return {'message': 'Please enter the new password'}, 400
        else:
            return {'message': 'Please enter the new password'}, 400


class Logout(Resource):
    @api.doc(responses={400: 'Bad Request', 401: 'Unauthorised', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @jwt_required
    def post(self, current_user):
        """Method to logout a user"""
        if current_user.login_status is True:
            if 'access-token' in request.headers:
                token = request.headers['access-token']
                response = Token.blacklist_token(token=token, user=current_user.username)
                return response
            else:
                return {"message": "Token is missing"}, 401
        else:
            return {"message": "Please first login to perform the action"}, 401


api.add_resource(Login, '/api/v2/login')
api.add_resource(Register, '/api/v2/auth/register')
api.add_resource(Logout, '/api/v2/auth/logout')
api.add_resource(Home, '/home')
api.add_resource(PasswordReset, '/api/v2/auth/reset-password')
