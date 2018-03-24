from flask import request, jsonify
from flask_restful import Resource
from app.app import app, api
from app.models import Business
from app.Authentication.views import jwt_required
from app.Business.search_model import search_by_name, search_by_category,\
    search_by_location, search_by_location_and_category


@app.route('/api/v2/businesses', methods=['POST'])
@jwt_required
def register_business(current_user):
    """method for adding a user"""
    business_data = request.get_json(force=True)
    business_name = business_data.get('business_name')
    business_owner_id = current_user.user_id
    business_email = business_data.get('business_email')
    business_location = business_data.get('business_location')
    business_nominal_capital = business_data.get('business_nominal_capital')
    business_category = business_data.get('business_category')
    if business_name and business_category and business_location and business_email and business_nominal_capital:
        if Business.is_valid_email(business_email) is True:
            my_business = Business.query.filter_by(business_name=business_name).first()
            if not my_business:
                my_business_email = Business.query.filter_by(business_email=business_email).first()
                if not my_business_email:
                    new_business = Business(business_owner_id=business_owner_id, business_name=business_name,
                                            business_email=business_email, business_location=business_location,
                                            business_nominal_capital=business_nominal_capital,
                                            business_category=business_category)

                    response = new_business.register_business(new_business)
                    response.status_code = 201
                    return response
                else:
                    return jsonify({"message": "Email already exists"})
            else:
                return jsonify({"message":"Business already exists"})
        else:
            return jsonify({"message":"Not a valid email address"})
    else:
        return jsonify({"message":"All fields are required, that is business_name, business_email,"
                                  "business_location, business_nominal_capital and business_category"})


class GetAllBusinesses(Resource):
    """Class for getting all the businesses"""
    def get(self):
        business_name= request.args.get('q')
        business_category = request.args.get('category')
        business_location = request.args.get('location')
        if business_name:
            my_search_result = search_by_name(business_name)
            return my_search_result

        elif business_category and not business_location:
           my_search_result = search_by_category(business_category)
           return my_search_result

        elif business_location and not business_category:
            my_search_result = search_by_location(business_location)
            return my_search_result
        elif business_category and business_location:
            my_search_result = search_by_location_and_category(business_location, business_category)
            return my_search_result
        else:
            response = Business.get_all_businesses()
            return response


class GetSpecificBusiness(Resource):
    """class to obtain a single business"""
    def get(self, business_id):
        response = Business.get_specific_business(business_id=business_id)
        return response


@app.route('/api/v2/businesses/<business_id>', methods=['PUT','DELETE'])
@jwt_required
def business_operations(current_user, business_id):
    if request.method == "DELETE":
        if current_user:
            delete_this_business = Business.delete_business(business_id=business_id,
                                                            user_id=current_user.user_id)
            response = delete_this_business
            return response
        else:
            return jsonify('You are currently not logged in to perform this action')
    if request.method == "PUT":
        """Edit a business"""
        business_data = request.get_json(force=True)
        business_name = business_data.get('business_name')
        business_email = business_data.get('business_email')
        business_location = business_data.get('business_location')
        business_nominal_capital = business_data.get('business_nominal_capital')
        business_category = business_data.get('business_category')
        if business_email:
            if Business.is_valid_email(business_email) is True:
                response = Business.update_business(business_id,current_user,business_name,business_email,
                                                    business_location, business_nominal_capital,
                                                    business_category)
                return response
            else:
                return jsonify({"message": "Not a valid email address"})
        else:
            response = Business.update_business(business_id, current_user, business_name, business_email,
                                                business_location, business_nominal_capital,
                                                business_category)
            return response


# api.add_resource(RegisterBusiness, '')
api.add_resource(GetAllBusinesses, '/api/v2/businesses')
api.add_resource(GetSpecificBusiness, '/api/v2/businesses/<business_id>')
# api.add_resource(UpdateBusinessProfile, '/api/v2/businesses/<business_id>')
# api.add_resource(DeleteBusiness, '/api/v2/businesses/<business_id>')
