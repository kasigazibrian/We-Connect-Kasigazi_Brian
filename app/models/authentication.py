"""Authentication model"""
from werkzeug.security import check_password_hash
import jwt
from app.app import app, db
from datetime import datetime, timedelta
from sqlalchemy import exc


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
        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"Message": "User with that username not found. Please register", "Status": "Fail"}, 400
        if check_password_hash(user.password, password)is False:
            return {'Message': "Your username or password is incorrect", "Status": "Fail"}, 400
        if user.login_status is True:
            return {"Message": "You are currently logged in.", "Status": "Fail"}, 401
        token = jwt.encode(
            {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=60)},
            app.config['SECRET_KEY'])
        decoded_token = token.decode('utf-8')
        result = Token.add_token(token=decoded_token, token_owner_id=user.user_id)
        if result is None:
            return {'Message': 'Database error. Please contact administrator ', 'Status': 'Fail'}, 500
        user.login_status = True
        db.session.commit()
        return {'Token': decoded_token,
                'Message': 'You have successfully logged in',
                'Status': 'Success',
                'User': {'username': user.username,
                         'email': user.email,
                         'first_name': user.first_name,
                         'last_name': user.last_name,
                         'gender': user.gender
                         }
                }, 201

    @staticmethod
    def add_user(user):
        """Register a user"""
        try:
            db.session.add(user)
            db.session.commit()
            return {'Message': 'User ' + user.first_name + ' has been registered successfully',
                    "status": "Success"}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {'Message': 'An error occurred. Please contact administrator', "Status": "Fail"}, 400

    @staticmethod
    def reset_password(current_user, password):
        """reset user password"""
        user = User.query.filter_by(user_id=current_user.user_id).first()
        if not user:
            return {"Message": "User not found. Please register", "Status": "Fail"}, 400
        user.password = password
        db.session.commit()
        return {"Message": "Password has been reset successfully", "Status": "Success"}, 201


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
            user = User.query.filter_by(username=user).first()
            user.login_status = False
            token = Token.query.filter_by(token=token).first()
            token.blacklist = True
            db.session.commit()
            return {'Message': 'You have successfully logged out', "Status": "Success"}, 201
        except exc.ArgumentError:
            db.session.rollback()
            return {'Message': 'Database error. Please contact administrator ', 'Status': 'Fail'}, 500

    @staticmethod
    def is_blacklisted(token):
        token = Token.query.filter_by(token=token).first()
        if token is None:
            return {'Message': 'Token error', "status": "Fail"}
        if token.blacklist is True:
            return True
        return False

    @staticmethod
    def add_token(token, token_owner_id):
        tkn = Token.query.filter_by(token=token).first()
        if not tkn:
            try:
                token = Token(token=token, token_owner_id=token_owner_id)
                db.session.add(token)
                db.session.commit()
                return token
            except exc.DatabaseError:
                db.session.rollback()
                return None
        return None


