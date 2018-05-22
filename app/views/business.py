"""Businesses views python file"""
from flask import request
from flask_restplus import Resource, fields, reqparse
from app import api
from app.models.business import Business
from app.views.authentication import jwt_required, authorizations
from app.models.utilities import Utilities
import os


business_model = api.model('Business', {'business_name': fields.String('Business Name'),
                                        'business_email': fields.String('Business Email'),
                                        'business_location': fields.String('Business Location'),
                                        'business_category': fields.String('Business Category'),
                                        'contact_number': fields.String('Contact Number'),
                                        'business_description': fields.String('Business Description')
                                        })


api.authorizations = authorizations
parser = reqparse.RequestParser()
parser.add_argument(name='page', type=int, location='args', help='Start should be an integer value')
parser.add_argument(name='limit', type=int, location='args', help='Limit should be an integer value')
parser.add_argument(name='category', type=str, location='args', help='Business Category')
parser.add_argument(name='location', type=str, location='args', help='Business Location')
parser.add_argument(name='q', type=str, location='args', help='Business Name')


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
        business_description = business_data.get('business_description')
        business_owner_id = current_user.user_id
        if not business_name or not business_category or not business_location or not business_email or not \
                contact_number or not business_description:
            return {"Message": "All fields are required, that is business_name, business_email,"
                               "business_location, business_category and "
                               "business_description", "Status": "Fail"}, 400

        if Utilities.is_valid_email(business_email) is False:
            return {"Message": "Not a valid email address", "Status": "Fail"}, 400
        if Utilities.is_valid_phone_number(contact_number) is False:
            return {"Message": "Not a valid phone number. Ensure it has ten digits", "Status": "Fail"}, 400
        business = Business.query.filter_by(business_name=business_name).first()
        if business is not None:
            return {"Message": "Business with this name already exists", "Status": "Fail"}, 400
        business = Business.query.filter_by(business_email=business_email).first()
        if business is not None:
            return {"Message": "Business with this email address already exists", "Status": "Fail"}, 400
        new_business = Business(business_owner_id=business_owner_id, business_name=business_name,
                                business_email=business_email, business_location=business_location,
                                contact_number=contact_number, business_category=business_category,
                                business_description=business_description)

        response = new_business.register_business(new_business)
        return response

    @api.expect(parser)
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    def get(self):
        """Method to obtain all registered businesses"""
        business_name = request.args.get('q')
        business_category = request.args.get('category')
        business_location = request.args.get('location')
        limit = request.args.get('limit', "20")
        page = request.args.get('page', "1")
        url = os.environ.get('base_url', "http://localhost:5000/")
        url = url + '/api/v2/businesses'

        search_result = Business.search_for_business(business_name=business_name, location=business_location,
                                                     category=business_category, limit=limit, page=page, url=url)
        return search_result


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
        response = Business.delete_business(business_id=business_id,
                                            user_id=current_user.user_id)
        return response

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
        business_description = business_data.get('business_description')
        if not business_name and not business_category and not business_location and not business_email and not \
                contact_number and not business_description:
            return {"Message": "Please enter at least one value for the field you would like to edit.",
                    "Status": "Fail"}, 400
        if not business_email == "":
            if Utilities.is_valid_email(business_email) is False:
                return {"Message": "Not a valid email address", 'Status': 'Fail'}, 400
            response = Business.update_business(business_id, current_user, business_name, business_email,
                                                business_location, contact_number,
                                                business_category, business_description)
            return response
        response = Business.update_business(business_id, current_user, business_name, business_email,
                                            business_location, contact_number,
                                            business_category, business_description)
        return response


api.add_resource(Businesses, '/api/v2/businesses')
api.add_resource(BusinessOperations, '/api/v2/businesses/<business_id>')
