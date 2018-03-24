from app.models import Business
from flask import jsonify


def search_by_name(business_name):
    """search for business based on its name"""
    business_search_result = Business.query.filter_by(business_name=business_name).first()
    if business_search_result:
        return jsonify({"business_name": business_search_result.business_name,
                        "business_email": business_search_result.business_email,
                        "business_location": business_search_result.business_location,
                        "business_nominal_capital": business_search_result.business_nominal_capital,
                        "business_category": business_search_result.business_category,
                        "business_id": business_search_result.business_id,
                        "business_owner_id": business_search_result.business_owner_id
                        })
    else:
        return jsonify({"message": "Business has not been found"})


def search_by_category(business_category):
    """Search for business based on category"""
    business_search_result = Business.query.filter_by(business_category=business_category).all()
    if business_search_result:
        registered_businesses = []
        for business in business_search_result:
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
    else:
        return jsonify({"message": "Business has not been found"})


def search_by_location(business_location):
    """search for business based on location"""
    business_search_result = Business.query.filter_by(business_location=business_location).all()
    if business_search_result:
        registered_businesses = []
        for business in business_search_result:
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
    else:
        return jsonify({"message": "Business has not been found"})


def search_by_location_and_category(business_location, business_category):
    """search for business based on location and category"""
    business_search_result = Business.query.filter_by(business_location=business_location).all()
    if business_search_result:
        search_result = [business for business in business_search_result if business.business_category == business_category]
        if search_result:
            registered_businesses = []
            for business in search_result:
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
        else:
            return jsonify({"message": "Business has not been found"})
    else:
        return jsonify({"message": "Business has not been found"})



