from werkzeug.security import check_password_hash
import jwt
from app.app import app, db
from datetime import datetime, timedelta
from sqlalchemy import exc
import re


class User(db.Model):
    """class model for the user"""
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.VARCHAR(100), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    business_owner = db.relationship('Business', backref='owner', lazy='dynamic')
    token_owner = db.relationship('Token', backref='tk_owner', lazy='dynamic')
    login_status = db.Column(db.Boolean, default=False)

    def __init__(self, username, password, first_name, last_name, email, gender, login_status):
        """initialise a user"""
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.login_status = login_status

    @staticmethod
    def login(username, password):
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    if user.login_status is False:
                        token = jwt.encode(
                            {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=60)},
                            app.config['SECRET_KEY'])
                        decoded_token = token.decode('utf-8')
                        result = Token.add_token(token=decoded_token, token_owner_id=user.user_id)
                        if result == "added":
                            user.login_status = True
                            db.session.commit()
                            return {'token': decoded_token,
                                    'message': 'You have successfully logged in',
                                    'username': user.username,
                                    'email': user.email,
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'gender': user.gender,
                                    'status': 'Success'
                                    }, 201
                        else:
                            return {"message": "Database error. Please contact administrator", "status": "Fail"}, 400
                    else:
                        return {"message": "You are currently logged in.", "status": "Fail"}, 401
                else:
                    return {'message': "Your username or password is incorrect", "status": "Fail"}, 400
            else:
                return {"message": "User not found. Please register", "status": "Fail"}, 400
        else:
            return {"message": "Both username and password are required", "status": "Fail"}, 400

    @staticmethod
    def add_user(user_data):
        """Register a user"""
        try:
            db.session.add(user_data)
            db.session.commit()
            return {'message': 'User ' + user_data.first_name + ' has been added successfully',
                    "status": "Success"}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'An error occurred. Please contact administrator', "status": "Fail"}, 400

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    @staticmethod
    def is_valid_gender(gender):
        if re.match(r"(^(?:m|M|male|Male|f|F|female|Female)$)", gender):
            return True
        else:
            return False

    @staticmethod
    def is_valid_phone_number(phone_number):
        if re.match(r"^\d{12}$", phone_number):
            return True
        else:
            return False

    @staticmethod
    def password_reset(current_user, password):
        """reset user password"""
        user = User.query.filter_by(user_id=current_user.user_id).first()
        if user:
            user.password = password
            db.session.commit()
            return {"message": "Password has been reset successfully", "status": "Success"}, 201
        else:
            return {'message': 'User not found', "status": "Fail"}, 400


class Token(db.Model):
    """class for deactivating token"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.VARCHAR(500), unique=True, nullable=False)
    token_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    blacklist = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token, token_owner_id):
        self.token = token
        self.token_owner_id = token_owner_id

    @staticmethod
    def blacklist_token(token, user):
        """add token to database"""
        try:
            my_user = User.query.filter_by(username=user).first()
            my_user.login_status = False
            my_token = Token.query.filter_by(token=token).first()
            my_token.blacklist = True
            db.session.commit()
            return {'message':'You have successfully logged out', "status": "Success"}, 201
        except exc.ArgumentError:
            db.session.rollback()
            return {'message':'Error accessing database', "status": "Fail"}, 500

    @staticmethod
    def check_blacklisted_token(token):
        my_token = Token.query.filter_by(token=token).first()
        if my_token:
            if my_token.blacklist is True:
                return True
            else:
                return False
        else:
            return {'message': 'Token error', "status": "Fail"}

    @staticmethod
    def add_token(token, token_owner_id):
        my_token = Token.query.filter_by(token=token).first()
        if not my_token:
            try:
                tkn = Token(token=token, token_owner_id=token_owner_id)
                db.session.add(tkn)
                db.session.commit()
                return "added"
            except:
                db.session.rollback()
                return {'message': 'Error accessing database', "status": "Fail"}, 500
        else:
            return {"message": "Token already exists", "status": "Fail"}, 400
