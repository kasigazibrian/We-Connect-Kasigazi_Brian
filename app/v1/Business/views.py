"""views.py"""
from flask_restplus import fields
from app.v1 import api
from app.v1.Business.models import Business
from flask_restplus import Resource
from app.v1.Authentication.views import jwt_required, authorizations
registered_businesses = []
api.authorizations = authorizations

business_model = api.model('Business', {'business_name': fields.String('Business Name'),
                                        'email': fields.String('Business Email'),
                                        'business_location': fields.String('Business Location'),
                                        'business_category': fields.String('Business Category'),
                                        'contact_number': fields.String('Contact Number')
                                        })
business_output_model = api.model('Business_out', {'business_name': fields.String('Business Name'),
                                                   'email': fields.String('Business Email'),
                                                   'business_location': fields.String('Business Location'),
                                                   'business_category': fields.String('Business Category'),
                                                   'business_owner':fields.String('Business Owner'),
                                                   'contact_number': fields.String('Contact Number')})


@api.route('/api/v1/businesses')
class Businesses(Resource):
    """Class for businesses"""
    @api.doc(security='api_key')
    @jwt_required
    @api.expect(business_model)
    def post(self, current_user):
        """Method for registering a business"""
        test_business = api.payload
        business_id = len(registered_businesses) + 1
        business_owner = current_user
        if 'business_name' in test_business:
            business_name = test_business['business_name']
        if 'business_location' in test_business:
            business_location = test_business['business_location']
        if 'business_category' in test_business:
            business_category = test_business['business_category']
        if 'email' in test_business:
            email = test_business['email']
        if 'contact_number' in test_business:
            contact_number = test_business['contact_number']
        my_business = [business for business in registered_businesses if business['business_name'] == business_name]
        check_email_availabilty = [business for business in registered_businesses
                                   if business['email'] == email]
        if not my_business:
            if not check_email_availabilty:
                if business_name and business_location and business_category \
                        and email and contact_number:
                    if Business.is_valid_email(email=email) is True:
                        new_business = Business(business_id=business_id,
                                                business_owner=business_owner,
                                                business_name=business_name,
                                                business_location=business_location,
                                                business_category=business_category, email=email,
                                                contact_number=contact_number)

                        res = Business.register_business(new_business)
                        registered_businesses.append(res)
                        return {"message": "Business " + business_name + " has been registered successfully"}, 201
                    else:
                        return {'message': 'Invalid email address'}, 200
                else:
                    return {'message': 'All details are required to register a business'}, 200
            else:
                return {'message': 'Email already exists'}, 200
        else:
            return {'message': 'Business already exists'}, 200

    @api.marshal_with(business_output_model, envelope='Businesses')
    def get(self):
        """Method for getting all businesses"""
        all_businesses = Business.get_all_businesses(registered_businesses)
        return all_businesses


@api.route('/api/v1/businesses/<int:business_id>')
class BusinessOperations(Resource):
    """Class for performing business operations"""
    @api.marshal_with(business_output_model, envelope='Business')
    def get(self, business_id):
        """Method to get a specific business"""
        my_business = Business.get_specific_business(business_id, registered_businesses)
        res = my_business
        return res, 200

    @jwt_required
    def delete(self, current_user, business_id):
        """Method to delete a business"""
        response = Business.delete_registered_business(business_owner= current_user,business_id=business_id,
                                                       registered_businesses= registered_businesses)
        return response

    @api.expect(business_model)
    @jwt_required
    def put(self, current_user, business_id):
        """method to update a business profile"""
        test_business = api.payload
        res = Business.update_registered_business(business_id=business_id,
                                                  business_owner= current_user,
                                                  registered_businesses=registered_businesses,
                                                  test_business=test_business)
        return res
