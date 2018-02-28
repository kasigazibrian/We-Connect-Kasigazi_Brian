"""Class Business"""
from flask import jsonify


class Business(object):
    """Business class for registering a new business"""
    def __init__(self, business_id, business_owner_id, business_name, business_location,
                 business_category, contact_number, email):
        self.business_id = business_id
        self.business_owner_id = business_owner_id
        self.business_name = business_name
        self.business_location = business_location
        self.business_category = business_category
        self.contact_number = contact_number
        self.email = email

    def __str__(self):
        return "Business(business_owner_id='%s')" % self.business_owner_id

    @staticmethod
    def register_business(business_data):
        # change the password to a new value
        res = ({
            'business_id': business_data.business_id,
            'business_owner_id': business_data.business_owner_id,
            'business_name': business_data.business_name,
            'business_category': business_data.business_category,
            'first_name': business_data.email,
            'last_name': business_data.business_location,
            'email': business_data.contact_number,
            'message': 'business created successfully'
        })
        return res

    @staticmethod
    def get_specific_business(business_id, businesses_registered):
        my_business = [business for business in businesses_registered if business['business_id'] == business_id]
        if my_business:
            return my_business
        else:
            return "Business not found"

    @staticmethod
    def update_registered_business( business_id, business_owner_id,registered_businesses, new_name):
        """ method allows a user update a registered business"""

        # check if user owns the business
        my_business = [business for business in registered_businesses if business['business_id'] == business_id]
        # check if business exists
        if my_business:
            # check for ownership
            if my_business['business_owner_id'] == business_owner_id:
                my_business['business_name'] = new_name

                return my_business
            else:
                return "Not enough privileges to perform action"
        else:
            return "Business does not exist"

    @staticmethod
    def delete_registered_business(business_owner_id,business_id, registered_businesses):
        """ method allows a user to delete a business they registered"""
        my_business = [business for business in registered_businesses if business['business_id'] == business_id]
        # check if business exists
        if my_business[0]:
            # check for ownership
            if my_business[0]['business_owner_id']== business_owner_id:
                registered_businesses.remove(my_business[0])
                return registered_businesses
            else:
                return "Not enough privileges to perform action"
        else:
            return "Business does not exist"

    @staticmethod
    def get_all_businesses(businesses):
        return businesses