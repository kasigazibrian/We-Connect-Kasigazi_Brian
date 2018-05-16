"""Businesses model"""
from app.app import db
from sqlalchemy import exc
from app.models.authentication import User
from app.models.utilities import Utilities


class Business(db.Model):
    """class model for the business"""
    business_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    business_name = db.Column(db.VARCHAR(100), nullable=False, unique=True)
    business_email = db.Column(db.VARCHAR(100), unique=True)
    business_location = db.Column(db.VARCHAR(150), nullable=False)
    contact_number = db.Column(db.VARCHAR(15))
    business_description = db.Column(db.VARCHAR(300))
    business_category = db.Column(db.VARCHAR(150))
    business_review = db.relationship('BusinessReviews', backref='review_owner', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, business_owner_id, business_name,business_email, business_location,
                 contact_number, business_category, business_description):
        """initialise a business"""
        self.business_owner_id = business_owner_id
        self.business_name = business_name
        self.business_email = business_email
        self.business_location = business_location
        self.contact_number = contact_number
        self.business_category = business_category
        self.business_description = business_description

    @staticmethod
    def to_json(businesses):
        business_list = []
        for business in businesses:
            business_data = {}
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            business_data['business_description'] = business.business_description
            business_list.append(business_data)
        if len(business_list) == 1:
            return {'Business': business_list, 'Status': 'Success'}, 200
        return {'Businesses': business_list, 'Status': 'Success'}, 200

    @staticmethod
    def register_business(business):
        """Register a business"""
        try:
            db.session.add(business)
            db.session.commit()
            return {"Message": "Business " + business.business_name + " has been registered successfully",
                    "Status": "Success"}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {'Message': 'Database error. Please contact administrator ', 'Status': 'Fail'}, 500

    @staticmethod
    def delete_business(business_id, user_id):
        """Delete a business"""
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return {'Message': 'You do not have enough privileges to delete this business. Please login',
                    "Status": "Fail"}, 401
        business = Business.query.filter_by(business_id=business_id).first()
        if not business:
            return {'Message': 'Business to be deleted not found', 'Status': 'Fail'}, 400
        if not business.business_owner_id == user_id:
            return {'Message': 'You do not have enough privileges to delete this business',
                    "Status": "Fail"}, 401
        db.session.delete(business)
        db.session.commit()
        return {"Message": "Business has been deleted successfully", "Status": "Success"}, 200

    @staticmethod
    def get_specific_business(business_id):
        """Get a specific business"""
        business_result = []
        business = Business.query.filter_by(business_id=business_id).first()
        if business is None:
            return {'Business': business_result, "Status": "Success"}, 400
        business_result.append(business)
        response = Business.to_json(business_result)
        return response

    @staticmethod
    def update_business(business_id, current_user, business_name, business_email, business_location,
                        contact_number, business_category, business_description):
        business = Business.query.filter_by(business_id=business_id).first()
        if business is None:
            return {'Message': 'Business not found', "Status": "Success"}, 400
        user = User.query.filter_by(user_id=current_user.user_id).first()
        if user is None:
            return {'Message': 'Not enough privileges to perform this action. Please login', "Status": "Fail"}, 401
        business = Business.query.filter_by(business_id=business_id).first()
        if not business:
            return {'Message': 'Business to be updated not found', 'Status': 'Fail'}, 400
        if not business.business_owner_id == current_user.user_id:
            return {'Message': 'Not enough privileges to perform action', "Status": "Fail"}, 401

        if business_name:
            business_in_db = Business.query.filter_by(business_name=business_name).first()
            if not business_in_db or (business_in_db and
                                           (business_in_db.business_id == business_id)):
                business.business_name = business_name
                db.session.commit()
            else:
                return {"Message": "Business with this name already exists", "Status": "Fail"}, 400
        if business_email:
            business_in_db = Business.query.filter_by(business_email=business_email).first()
            if not business_in_db or (business_in_db and
                                           (business_in_db.business_id == business_id)):
                business.business_email = business_email
                db.session.commit()
            else:
                return {"Message": "Business with this email already exists", "Status": "Fail"}, 400

        if business_location:
            business.business_location = business_location
            db.session.commit()

        if contact_number:
            if Utilities.is_valid_phone_number(contact_number) is False:
                return {"Message": "Not a valid phone number. Ensure it has ten digits", "Status": "Fail"}, 400
            business.contact_number = contact_number
            db.session.commit()

        if business_category:
            business.business_category = business_category
            db.session.commit()

        if business_description:
            business.business_description = business_description
            db.session.commit()
        return {'Message': 'Business updated successfully', "Status": "Success"}, 201

    @staticmethod
    def search_for_business(business_name="", location="", category="", limit=""):
        if business_name is not None:
            """search for business based on its name"""
            businesses = Business.query.filter(
                Business.business_name.ilike("%{}%".format(business_name)))
            if not businesses:
                return {"Businesses": [], 'Status': 'Success'}, 400
            if location is not None and category is None and limit is None:
                """filter businesses based on location"""
                businesses = businesses.filter(Business.business_location.ilike
                                                               ("%{}%".format(location))).all()
                if len(businesses) == 0:
                    return {"Businesses": [], 'Status': 'Success'}, 400
                response = Business.to_json(businesses)
                return response

            elif category is not None and location is None and limit is None:
                """filter businesses based on category"""
                businesses = businesses.filter(Business.business_category.ilike
                                                               ("%{}%".format(category))).all()
                if len(businesses) == 0:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                response = Business.to_json(businesses)
                return response

            elif category is not None and location is not None and limit is None:
                """ filter business based on location and category"""
                business_search_result = businesses.filter(Business.business_location.ilike
                                                               ("%{}%".format(location)))
                if not business_search_result:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                businesses = business_search_result.filter \
                    (Business.business_category.ilike("%{}%".format(category))).all()
                if len(businesses) == 0:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                response = Business.to_json(businesses)
                return response

            elif category is not None and limit is not None and location is None:
                """Search for business based on category"""
                business_search_result = businesses.filter(Business.business_category.ilike
                                                               ("%{}%".format(category)))
                if not business_search_result:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                try:
                    limit = int(limit)
                    businesses = business_search_result.paginate(per_page=limit, page=1, error_out=True).items
                    response = Business.to_json(businesses)
                    return response
                except ValueError:
                    return {"Message": "Make sure the limit is a valid integer value", 'Status': 'Fail'}, 400

            elif location is not None and limit is not None and category is None:
                """ search for business based on location"""
                business_search_result = businesses.filter \
                    (Business.business_location.ilike("%{}%".format(location)))
                if not business_search_result:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                try:
                    limit = int(limit)
                    businesses = business_search_result.paginate(page=1, per_page=limit, error_out=True).items
                    response = Business.to_json(businesses)
                    return response
                except ValueError:
                    return {"message": "Make sure the limit is a valid integer value", 'Status': 'Fail'}, 400

            elif location is not None and limit is not None and category is not None:
                """search for business based on location and category and limit results per page"""
                business_search_result = businesses.filter(Business.business_location.ilike
                                                               ("%{}%".format(location)))
                if not business_search_result:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                search_result = business_search_result.filter(Business.business_category.ilike
                                                              ("%{}%".format(category)))
                if not search_result:
                    return {"Businesses": [], 'Status': 'Success'}, 200
                try:
                    limit = int(limit)
                    businesses = search_result.paginate(per_page=limit, page=1, error_out=True).items
                    response = Business.to_json(businesses)
                    return response
                except ValueError:
                    return {'Message': 'Make sure the limit is a valid integer value', 'Status': 'Fail'}, 400

            elif limit is not None and location is None and category is None:
                """ limit number of businesses per page"""
                try:
                    limit = int(limit)
                    businesses = businesses.paginate(per_page=limit, page=1, error_out=True).items
                    if len(businesses) != 0:
                        response = Business.to_json(businesses)
                        return response
                    return {"Businesses": [], 'Status': 'Success'}, 200
                except ValueError:
                    return {"Message": "Make sure the limit is a valid integer value", 'Status': 'Fail'}, 400
            else:
                response = Business.to_json(businesses.all())
                return response

        else:
            """Get all businesses"""
            businesses = Business.query.all()
            if len(businesses) == 0:
                return {"Businesses": [], 'Status': 'Success'}, 200
            if limit is not None:
                try:
                    limit = int(limit)
                    businesses = Business.query.paginate(per_page=limit, page=1, error_out=True).items
                    response = Business.to_json(businesses)
                    return response
                except ValueError:
                    return {"Message": "Make sure the limit is a valid integer value", 'Status': 'Fail'}, 400
            response = Business.to_json(businesses)
            return response




