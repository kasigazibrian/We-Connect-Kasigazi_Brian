"""Businesses model"""
from app import db
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
    business_review = db.relationship('BusinessReviews',  backref='review_owner', lazy='dynamic')
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
            business_data = dict()
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            business_data['business_description'] = business.business_description
            business_list.append(business_data)
        return {'Businesses': business_list, 'Status': 'Success'}

    @staticmethod
    def register_business(business):
        """Register a business"""
        db.session.add(business)
        db.session.commit()
        return {"Message": "Business " + business.business_name + " has been registered successfully",
                "Status": "Success"}, 201

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
        return response, 200

    @staticmethod
    def update_business(business_id, current_user, business_name, business_email, business_location,
                        contact_number, business_category, business_description):
        business_id = int(business_id)
        business = Business.query.filter_by(business_id=business_id).first()
        if business is None:
            return {'Message': 'Business not found', "Status": "Fail"}, 400
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
            if business_in_db:
                if business_in_db.business_id != business_id:
                    return {"Message": "Business with this name already exists", "Status": "Fail"}, 400
            business.business_name = business_name
            db.session.commit()
        if business_email:
            business_in_db = Business.query.filter_by(business_email=business_email).first()
            if business_in_db:
                if business_in_db.business_id != business_id:
                    return {"Message": "Business with this email already exists", "Status": "Fail"}, 400
            business.business_email = business_email
            db.session.commit()
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
    def get_paginated_list(url, page, limit, results):
        """ Check if businesses exist """
        if Utilities.is_positive_number(limit) and Utilities.is_positive_number(page):
            limit = int(limit)
            page = int(page)
            businesses = results.paginate(per_page=limit, page=page, error_out=True)
            json_result = Business.to_json(businesses=businesses.items)
            count = businesses.total

            # make response
            business_object = dict()
            business_object['page'] = page
            business_object['limit'] = limit
            business_object['count'] = count
            business_object['number_of_pages'] = businesses.pages
            """ Make urls """
            # make previous url
            if not businesses.has_prev:
                business_object['previous'] = None
            else:
                page_copy = businesses.prev_num
                business_object['previous'] = url + '?limit=%d&page=%d' % (limit, page_copy)
            # make next url
            if not businesses.has_next:
                business_object['next'] = None
            else:
                page_copy = businesses.next_num
                business_object['next'] = url + '?limit=%d&page=%d' % (limit, page_copy)
            business_object['Businesses'] = json_result['Businesses']
            business_object['Status'] = "Success"
            return business_object, 200
        return {"Message": "Make sure the limit or page has a valid integer value", 'Status': 'Fail'}, 400

    @staticmethod
    def search_for_business(business_name="", location="", url="", category="", page="1", limit="20"):
        if business_name and not (location or category):
            """search for business based on its name"""

            businesses = Business.query.filter(
                Business.business_name.ilike("%{}%".format(business_name)))
            if not businesses:
                return {"Businesses": [], 'Status': 'Success'}, 400
            return Business.get_paginated_list(url=url, page=page, limit=limit, results=businesses)

        elif category and not (business_name or location):
            """filter businesses based on category"""

            businesses = Business.query.filter(Business.business_category.ilike
                                               ("%{}%".format(category)))
            if not businesses:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=businesses)
            return response

        elif (location and category) and not business_name:
            """ filter business based on location and category"""

            business_search_result = Business.query.filter(Business.business_location.ilike
                                                           ("%{}%".format(location)))
            if not business_search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            businesses = business_search_result.filter \
                (Business.business_category.ilike("%{}%".format(category)))
            if not businesses:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=businesses)
            return response

        elif (category and business_name) and not location:
            """Search for business based on category and business name"""
            business_search_result = Business.query.filter(Business.business_name.ilike
                                                           ("%{}%".format(business_name)))
            if not business_search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            businesses = business_search_result.filter \
                (Business.business_category.ilike("%{}%".format(category)))
            if not businesses:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=businesses)
            return response

        elif location and not (business_name or category):
            """ search for business based on location"""
            if not Utilities.is_valid_string(location):
                return {"Message": "Not a valid location", 'Status': 'Fail'}, 400
            business_search_result = Business.query.filter \
                (Business.business_location.ilike("%{}%".format(location)))
            if not business_search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=business_search_result)
            return response

        elif (business_name and location) and not category:
            """search for business based on location and business name"""
            if not Utilities.is_valid_string(location):
                return {"Message": "Not a valid location", 'Status': 'Fail'}, 400
            business_search_result = Business.query.filter(Business.business_name.ilike
                                                           ("%{}%".format(business_name)))
            if not business_search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            search_result = business_search_result.filter(Business.business_location.ilike
                                                          ("%{}%".format(location)))
            if not search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=search_result)
            return response

        elif business_name and location and category:
            """ Search for businesses based on business name, location and category"""
            business_search_result = Business.query.filter(Business.business_name.ilike
                                                           ("%{}%".format(business_name)))
            if not business_search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            search_result = business_search_result.filter(Business.business_location.ilike
                                                          ("%{}%".format(location)))
            if not search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            search_result = business_search_result.filter(Business.business_category.ilike
                                                          ("%{}%".format(category)))
            if not search_result:
                return {"Businesses": [], 'Status': 'Success'}, 200
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=search_result)
            return response

        else:
            """Get all businesses"""
            businesses = Business.query.all()
            if len(businesses) == 0:
                return {"Businesses": [], 'Status': 'Success'}, 200
            businesses = Business.query
            response = Business.get_paginated_list(url=url, page=page, limit=limit, results=businesses)
            return response






