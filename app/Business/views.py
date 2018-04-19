from flask import request
from flask_restplus import Resource, fields, reqparse
from app.app import api
from app.Business.models import Business
from app.Authentication.views import jwt_required
from app.Authentication.views import authorizations
from app.Business.search_model import search_by_name, search_by_category,\
    search_by_location, search_by_location_and_category, search_by_category_and_limit,\
    search_by_location_and_limit, search_by_limit, search_by_location_and_category_and_limit
business_model = api.model('Business', {'business_name': fields.String('Business Name'),
                                        'business_email': fields.String('Business Email'),
                                        'business_location': fields.String('Business Location'),
                                        'business_category': fields.String('Business Category'),
                                        'contact_number': fields.String('Contact Number')
                                        })
business_output_model = api.model('Business_out', {'business_name': fields.String('Business Name'),
                                                   'business_email': fields.String('Business Email'),
                                                   'business_location': fields.String('Business Location'),
                                                   'business_category': fields.String('Business Category'),
                                                   'business_owner_id':fields.String('Business Owner Id'),
                                                   'contact_number': fields.String('Contact Number')})
api.authorizations = authorizations
api.authorizations = authorizations
parser = reqparse.RequestParser()
parser.add_argument( name='limit', type=int, location='args', help='Limit should be an integer value')
parser.add_argument( name='category', type=str, location='args', help='Business Category')
parser.add_argument( name='location', type=str, location='args', help='Business Location')
parser.add_argument( name='q', type=str, location='args', help='Business Name')


class Businesses(Resource):
    """Class for registering a user"""
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @api.expect(business_model)
    @jwt_required
    def post(self, current_user):
        """Method for registering a business"""
        business_data = api.payload
        business_name = business_data.get('business_name')
        business_email = business_data.get('business_email')
        business_location = business_data.get('business_location')
        contact_number = business_data.get('contact_number')
        business_category = business_data.get('business_category')
        business_owner_id = current_user.user_id
        if business_name and business_category and business_location and business_email and contact_number:
            if Business.is_valid_email(business_email) is True:
                if Business.is_valid_phone_number(contact_number):
                    my_business = Business.query.filter_by(business_name=business_name).first()
                    if not my_business:
                        my_business_email = Business.query.filter_by(business_email=business_email).first()
                        if not my_business_email:
                            new_business = Business(business_owner_id=business_owner_id, business_name=business_name,
                                                    business_email=business_email, business_location=business_location,
                                                    contact_number=contact_number,
                                                    business_category=business_category)

                            response = new_business.register_business(new_business)
                            return response
                        else:
                            return {"message": "Email already exists", "status": "Fail"}, 400
                    else:
                        return {"message": "Business already exists", "status": "Fail"}, 400
                else:
                    return {"message": "Not a valid phone number. Ensure it has ten digits", "status": "Fail"}, 400
            else:
                return {"message": "Not a valid email address", "status": "Fail"}, 400
        else:
            return {"message": "All fields are required, that is business_name, business_email,"
                               "business_location, business_nominal_capital and business_category",
                    "status": "Fail"}, 400

    # @api.marshal_with(business_output_model)
    @api.expect(parser)
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    def get(self):
        """Method to obtain registered businesses"""
        business_name = request.args.get('q')
        business_category = request.args.get('category')
        business_location = request.args.get('location')
        limit = request.args.get('limit')

        if business_name:
            my_search_result = search_by_name(business_name)
            return my_search_result

        elif business_category and not business_location and not limit:
            my_search_result = search_by_category(business_category)
            return my_search_result

        elif business_location and not business_category and not limit:
            my_search_result = search_by_location(business_location)
            return my_search_result
        elif business_category and business_location and not limit:
            my_search_result = search_by_location_and_category(business_location, business_category)
            return my_search_result
        elif limit and not business_category and not business_location:
            my_search_result = search_by_limit(limit)
            return my_search_result
        elif limit and business_category and not business_location:
            my_search_result = search_by_category_and_limit(business_category, limit)
            return my_search_result
        elif limit and business_location and not business_category:
            my_search_result = search_by_location_and_limit(business_location, limit)
            return my_search_result
        elif limit and business_location and business_category:
            my_search_result = search_by_location_and_category_and_limit(business_location, business_category, limit)
            return my_search_result
        else:
            response = Business.get_all_businesses()
            return response


class BusinessOperations(Resource):
    """class to obtain a single business"""
    # @api.marshal_with(business_output_model)
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    def get(self, business_id):
        """Method to obtain a specific business"""
        response = Business.get_specific_business(business_id=business_id)
        return response

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @jwt_required
    def delete(self, current_user, business_id):
        """Method to delete a registered business"""
        if current_user:
            delete_this_business = Business.delete_business(business_id=business_id,
                                                            user_id=current_user.user_id)
            response = delete_this_business
            return response
        else:
            return {'message': 'You are currently not logged in to perform this action'}, 400

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'},
             security='api_key')
    @api.expect(business_model)
    @jwt_required
    def put(self, current_user, business_id):
        """Edit a business"""
        business_data = api.payload
        business_name = business_data.get('business_name')
        business_email = business_data.get('business_email')
        business_location = business_data.get('business_location')
        contact_number = business_data.get('contact_number')
        business_category = business_data.get('business_category')
        if business_email:
            if Business.is_valid_email(business_email) is True:
                response = Business.update_business(business_id, current_user, business_name, business_email,
                                                    business_location, contact_number,
                                                    business_category)
                return response
            else:
                return {"message": "Not a valid email address"}, 400
        else:
            response = Business.update_business(business_id, current_user, business_name, business_email,
                                                business_location, contact_number,
                                                business_category)
            return response


api.add_resource(Businesses, '/api/v2/businesses')
api.add_resource(BusinessOperations, '/api/v2/businesses/<business_id>')
