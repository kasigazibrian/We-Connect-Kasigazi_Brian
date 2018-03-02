"""views.py"""
from flask import request, jsonify
from app.v1 import app, api
from app.v1.Business.models import Business
from flask_restful import Resource
from functools import wraps
import jwt

business = {}

sample_registered_businesses = [{
    'business_id': '1',
    'business_owner_id': 1,
    'business_name': 'media studios',
    'business_category': 'entertainment',
    'business_location': 'kampala',
    'email': 'supercom@gmail.com',
    'contact_number': '256781712929'
},
    {
        'business_id': '2',
        'business_owner_id': '2',
        'business_name': 'real houses',
        'business_category': 'real estate',
        'business_location': 'kabale',
        'email': 'real@gmail.com',
        'contact_number': '256781712928'
    }
]

def jwt_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            if token:
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'])
                    current_user = data['username']
                except:
                    return jsonify({'message': 'Token is missing'})
            else:
                return jsonify({'message': 'Token is missing'})
        else:
            return jsonify({'message': 'Token is missing'})
        return f(current_user, *args, **kwargs)
    return decorated


class Businesses(Resource):
    """Class for businesses"""
    def post(self):
        """Method for registering a business"""
        test_business = request.get_json(force=True)
        business_id = test_business.get('business_id')
        business_owner_id = test_business.get('business_owner_id')
        business_name = test_business.get('business_name')
        business_location = test_business.get('business_location')
        business_category = test_business.get('business_category')
        email = test_business.get('email')
        contact_number = test_business.get('contact_number')
        if business_id and business_owner_id and business_name and business_location and business_category \
                and email and contact_number:
            new_business = Business(business_id=business_id,
                                    business_owner_id=business_owner_id,
                                    business_name=business_name,
                                    business_location=business_location,
                                    business_category=business_category, email=email,
                                    contact_number=contact_number)

            res = Business.register_business(new_business)
            sample_registered_businesses.append(res)
            return jsonify(res)
        else:
            return jsonify({'message': 'All details are required to register a business'})

    def get(self):
        """Method for getting all businesses"""
        all_businesses = Business.get_all_businesses(sample_registered_businesses)

        return jsonify({"Businesses": all_businesses})


class BusinessOperations(Resource):
    """Class for performing business operations"""
    def get(self, business_id):
        """Method to get a specific business"""
        my_business = Business.get_specific_business(business_id, sample_registered_businesses)
        res = jsonify({
            'business': my_business
        })
        res.status_code = 200
        return res

    @jwt_required
    def delete(self, current_user, business_id):
        """Method to delete a business"""
        if current_user:
            response = Business.delete_registered_business(business_owner_id=1,business_id=business_id,
                                                            registered_businesses=sample_registered_businesses)
            return jsonify({'Businesses': response})

    @jwt_required
    def put(self, current_user, business_id):
        """method to update a business profile"""
        if current_user:
            new_name=request.get_json()
            res = Business.update_registered_business(business=sample_registered_businesses,business_id=business_id,
                                                       business_owner_id=1)
            return jsonify({"Business": res})


api.add_resource(Businesses, '/api/v1/businesses')
api.add_resource(BusinessOperations,'/api/v1/businesses/<business_id>')
