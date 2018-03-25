"""models.py"""
from flask import jsonify
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
    def login( username, password):
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.login_status is False:
                    if check_password_hash(user.password, password):
                        token = jwt.encode(
                            {'username': user.username, 'exp': datetime.utcnow() + timedelta(minutes=2)},
                            app.config['SECRET_KEY'])
                        decoded_token = token.decode('utf-8')
                        result =Token.add_token(token=decoded_token, token_owner_id=user.user_id)
                        if result=="added":
                            user.login_status = True
                            db.session.commit()
                            return jsonify({'token': decoded_token, 'message': 'You have successfully logged in'})
                        else:
                            return jsonify({"message":"Database error. Please contact administrator"})
                    else:
                        return jsonify({'message':"Your username or password is incorrect"})
                else:
                    return jsonify({"message":"You are currently logged in."})
            else:
                return jsonify({"message":"User not found. Please register"})
        else:
            return jsonify({"message":"Both username and password are required"})

    @staticmethod
    def add_user(user_data):
        """Register a user"""
        try:
            db.session.add(user_data)
            db.session.commit()
            return jsonify({'message': 'User added successfully'})
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify({'message': 'An error occurred. Please contact administrator'})

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    @staticmethod
    def is_valid_gender(gender):
        if re.match(r"(^(?:m|M|male|Male|f|F|female|Female)$)",gender):
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
            return jsonify({"message":"Password has been reset successfully"})
        else:
            return jsonify({'message': 'User not found'})


class Business(db.Model):
    """class model for the business"""
    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    business_name = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    business_email = db.Column(db.VARCHAR(100), unique=True)
    business_location = db.Column(db.VARCHAR(150), nullable=False)
    business_nominal_capital = db.Column(db.FLOAT)
    business_category = db.Column(db.VARCHAR(150))
    business_review = db.relationship('BusinessReviews', backref='review_owner', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, business_owner_id, business_name,business_email, business_location,
                 business_nominal_capital, business_category):
        """initialise a business"""
        self.business_owner_id = business_owner_id
        self.business_name = business_name
        self.business_email = business_email
        self.business_location = business_location
        self.business_nominal_capital = business_nominal_capital
        self.business_category = business_category

    @staticmethod
    def register_business(business_data):
        """Register a business"""
        try:
            db.session.add(business_data)
            db.session.commit()
            return jsonify({'message': 'Business has been registered successfully'})
        except exc.IntegrityError:
            db.session.rollback()
            return jsonify({'message':'An error occurred. Please contact administrator '})

    @staticmethod
    def delete_business( business_id, user_id):
        """Delete a business"""
        my_user =  User.query.filter_by(user_id=user_id).first()
        if my_user:
            relation = my_user.business_owner.filter_by(business_id=business_id).first()
            if relation:
                delete_business = Business.query.filter_by(business_id=business_id).first()
                if delete_business:
                    if relation.business_owner_id == user_id:
                        db.session.delete(delete_business)
                        db.session.commit()
                        return jsonify({"message": "Business has been deleted successfully"})
                    else:
                        return jsonify({'message': 'You do not have enough privileges to delete this business'})
                else:
                    return jsonify({'message': 'Business not found'})
            else:
                return jsonify({'message': 'You do not have enough privileges to delete this business'})
        else:
            return jsonify({'message': 'You do not have enough privileges to delete this business'})

    @staticmethod
    def get_specific_business(business_id):
        """Get a specific business"""
        business = Business.query.filter_by(business_id=business_id).first()
        business_data = {}
        if business:
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['business_nominal_capital'] = business.business_nominal_capital
            business_data['business_category'] = business.business_category
            return jsonify({'Business': business_data})
        else:
            return jsonify({'message': 'Business does not exist'})

    @staticmethod
    def get_all_businesses():
        """Get all businesses"""
        businesses = Business.query.all()
        if businesses:
            registered_businesses = []
            for business in businesses:
                business_data = {}
                business_data['business_id'] = business.business_id
                business_data['business_owner_id'] = business.business_owner_id
                business_data['business_name'] = business.business_name
                business_data['business_email'] = business.business_email
                business_data['business_location'] = business.business_location
                business_data['business_nominal_capital'] = business.business_nominal_capital
                business_data['business_category'] = business.business_category
                registered_businesses.append(business_data)
            return jsonify({'Businesses': registered_businesses})

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    @staticmethod
    def update_business(business_id, current_user, business_name, business_email, business_location,
                        business_nominal_capital,business_category):
        business = Business.query.filter_by(business_id=business_id).first()
        if business:
            relation = User.query.filter_by(user_id=current_user.user_id).first()
            business_possessor = relation.business_owner.filter_by(business_id=business_id).first()
            if business_possessor:
                if business_possessor.business_owner_id == current_user.user_id:
                    if business_name:
                        try:
                            business.business_name = business_name
                            db.session.commit()
                        except exc.IntegrityError:
                            return jsonify({"message": "Business name already exists"})
                    if business_email:
                        business.business_email = business_email
                        db.session.commit()
                    if business_location:
                        business.business_location = business_location
                        db.session.commit()
                    if business_nominal_capital:
                        business.business_nominal_capital = business_nominal_capital
                        db.session.commit()
                    if business_category:
                        business.business_category = business_category
                        db.session.commit()
                    return jsonify({'message': 'Business updated successfully'})
                else:
                    return jsonify({'messsage': 'Not enough privilege to perform action'})
            else:
                return jsonify({'messsage': 'Not enough privilege to perform action'})
        else:
            return jsonify({'message': 'Business not found'})


class BusinessReviews(db.Model):
    """Class model for business reviews"""
    review_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'))
    review = db.Column(db.VARCHAR(400))

    def __init__(self, business_id, review):
        self.business_id = business_id
        self.review = review

    @staticmethod
    def add_review(review_data):
        try:
            db.session.add(review_data)
            db.session.commit()
            return jsonify({'message': 'Review has been added successfully'})
        except:
            db.session.rollback()
            return jsonify({'message': 'An error occurred. Please contact administrator '})

    @staticmethod
    def get_all_reviews( business_id):
        all_reviews = BusinessReviews.query.filter_by(business_id=business_id).all()
        if all_reviews:
            reviews_added = []
            for my_review in all_reviews:
                review_data = {}
                review_data['business_id'] = my_review.business_id
                review_data['business_owner_id'] = my_review.review
                reviews_added.append(review_data)
            return jsonify({'Businesses': reviews_added})
        else:
            return jsonify({'message': 'No business reviews have been added yet'})


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
            return jsonify({'message':'You have successfully logged out'})
        except exc.ArgumentError:
            db.session.rollback()
            return jsonify({'message':'Error accessing database'})

    @staticmethod
    def check_blacklisted_token(token):
        my_token = Token.query.filter_by(token=token).first()
        if my_token.blacklist is True:
            return True
        else:
            return False

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
                return jsonify({'message': 'Error accessing database'})
        else:
            return jsonify({"message": "Token already exists"})


