"""Authentication views python file"""
from flask import request
from flask_restplus import Resource, fields
from app.app import app, api, db
from werkzeug.security import generate_password_hash
from app.models.authentication import User, Token
import jwt
from functools import wraps
from app.models.utilities import Utilities

authorizations = {'api_key': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'access-token'

}}


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return {'Message': 'Token is missing'}, 401
        if Token.is_blacklisted(token=token) is True:
            return {"Message": "Your session has expired!. Please login again", "Status": "Fail"}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            try:
                token = Token.query.filter_by(token=token).first()
                token.tk_owner.login_status = False
                token.blacklist = True
                db.session.commit()
                return {"Message": "Your session has expired!. Please login again", "Status": "Fail"}, 401
            except AttributeError:
                return {'Message': 'Token provided is invalid.', "Status": "Fail"}, 401
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
        return {'Message': 'You are Welcome! You can access the documentation on /', "Status": "Success"}, 200


class Register(Resource):
    """class for registering a user"""

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created'})
    @api.expect(User_model)
    def post(self):
        """Method to register a user"""
        new_user = api.payload
        username = new_user.get('username')
        password = new_user.get('password')
        first_name = new_user.get('first_name')
        last_name = new_user.get('last_name')
        email = new_user.get('email')
        gender = new_user.get('gender')
        if not username or not password or not first_name or not last_name or not \
                email or not gender:
            return {'Message': 'All fields are required, that is username,'
                               ' password, first_name, last_name, email and gender', "Status": "Fail"}, 400
        if Utilities.is_valid_email(email) is False:
            return {"Message": "Not a valid email address", "Status": "Fail"}, 400
        if Utilities.is_valid_gender(gender) is False:
            return {'Message': 'Invalid gender. Try Male, Female, M, F', "Status": "Fail"}, 400
        if User.query.filter_by(username=username).first():
            return {'Message': 'User with that username already exists', "Status": "Fail"}, 400
        if User.query.filter_by(email=email).first():
            return {"Message": "User with that email address already exists", "Status": "Fail"}, 400
        login_status = False
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password, first_name=first_name,
                        last_name=last_name, email=email, gender=gender,
                        login_status=login_status)

        response = User.add_user(new_user)
        return response


class Login(Resource):
    """Class for logging in a user"""

    @api.expect(login_model)
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created'})
    def post(self):
        """Logs in a user"""
        test_user = api.payload
        username = test_user.get('username')
        password = test_user.get('password')
        if not username or not password:
            return {"message": "Both username and password are required", "Status": "Fail"}, 400
        response = User.login(username=username, password=password)
        return response


class PasswordReset(Resource):
    """Class for resetting a user password"""

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @jwt_required
    @api.expect(new_password_model)
    def post(self, current_user):
        """Reset user password post request"""
        data = api.payload
        new_password = data.get('new_password')
        if not new_password:
            return {'Message': 'Please enter the new password', "Status": "Fail"}, 400
        new_password = generate_password_hash(new_password, method='sha256')
        response = User.reset_password(current_user, new_password)
        return response


class Logout(Resource):
    @api.doc(
        responses={400: 'Bad Request', 401: 'Unauthorised', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
        security='api_key')
    @jwt_required
    def post(self, current_user):
        """Method to logout a user"""
        if current_user.login_status is False:
            return {"Message": "Please first login to perform the action", "Status": "Fail"}, 401
        if 'access-token' not in request.headers:
            return {"Message": "Token is missing", "Status": "Fail"}, 401
        token = request.headers['access-token']
        response = Token.blacklist_token(token=token, user=current_user.username)
        return response


api.add_resource(Login, '/api/v2/login')
api.add_resource(Register, '/api/v2/auth/register')
api.add_resource(Logout, '/api/v2/auth/logout')
api.add_resource(Home, '/home')
api.add_resource(PasswordReset, '/api/v2/auth/reset-password')
