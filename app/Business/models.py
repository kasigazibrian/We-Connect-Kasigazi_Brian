from app.app import db
from sqlalchemy import exc
from app.Authentication.models import User
import re


class Business(db.Model):
    """class model for the business"""
    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    business_name = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    business_email = db.Column(db.VARCHAR(100), unique=True)
    business_location = db.Column(db.VARCHAR(150), nullable=False)
    contact_number = db.Column(db.VARCHAR(15))
    business_category = db.Column(db.VARCHAR(150))
    business_review = db.relationship('BusinessReviews', backref='review_owner', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, business_owner_id, business_name,business_email, business_location,
                 contact_number, business_category):
        """initialise a business"""
        self.business_owner_id = business_owner_id
        self.business_name = business_name
        self.business_email = business_email
        self.business_location = business_location
        self.contact_number = contact_number
        self.business_category = business_category

    @staticmethod
    def register_business(business_data):
        """Register a business"""
        try:
            db.session.add(business_data)
            db.session.commit()
            return {'message': 'Business has been registered successfully'}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {'message':'An error occurred. Please contact administrator '}, 500

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
                        return {"message": "Business has been deleted successfully", "status": "Success"}, 200
                    else:
                        return {'message': 'You do not have enough privileges to delete this business',
                                "status": "Fail"}, 401
                else:
                    return {'message': 'Business not found', "status": "Fail"}, 400
            else:
                return {'message': 'You do not have enough privileges to delete this business', "status": "Fail"}, 401
        else:
            return {'message': 'You do not have enough privileges to delete this business', "status": "Fail"}, 401

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
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            return {'Business': business_data, "status": "Success"}, 200
        else:
            return {'message': 'Business does not exist', "status": "Fail"}, 400

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
                business_data['contact_number'] = business.contact_number
                business_data['business_category'] = business.business_category
                registered_businesses.append(business_data)
            return {'Businesses': registered_businesses, "status": "Success"}, 200

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
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
    def update_business(business_id, current_user, business_name, business_email, business_location,
                        contact_number, business_category):
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
                            return {"message": "Business name already exists", "status": "Fail"}, 400
                    if business_email:
                        business.business_email = business_email
                        db.session.commit()
                    if business_location:
                        business.business_location = business_location
                        db.session.commit()
                    if contact_number:
                        business.contact_number = contact_number
                        db.session.commit()
                    if business_category:
                        business.business_category = business_category
                        db.session.commit()
                    return {'message': 'Business updated successfully', "status": "Success"}, 201
                else:
                    return {'messsage': 'Not enough privilege to perform action', "status": "Fail"}, 401
            else:
                return {'messsage': 'Not enough privilege to perform action', "status": "Fail"}, 401
        else:
            return {'message': 'Business not found', "status": "Fail"}, 400