"""Class Business"""
import re


class Business(object):
    """Business class for registering a new business"""
    def __init__(self, business_id, business_owner, business_name, business_location,
                 business_category, contact_number, email):
        self.business_id = business_id
        self.business_owner = business_owner
        self.business_name = business_name
        self.business_location = business_location
        self.business_category = business_category
        self.contact_number = contact_number
        self.email = email

    def __str__(self):
        return "Business(business_id='%s')" % self.business_id

    @staticmethod
    def register_business(business_data):
        # change the password to a new value
        res = {
            'business_id': business_data.business_id,
            'business_owner': business_data.business_owner,
            'business_name': business_data.business_name,
            'business_category': business_data.business_category,
            'email': business_data.email,
            'business_location': business_data.business_location,
            'contact_number': business_data.contact_number
        }
        return res

    @staticmethod
    def get_specific_business(business_id, businesses_registered):
        my_business = [business for business in businesses_registered if business['business_id'] == business_id]
        if my_business:
            return my_business[0]
        else:
            return "Business not found"

    @staticmethod
    def update_registered_business( business_id, business_owner,registered_businesses,test_business):
        """ method allows a user update a registered business"""
        my_business = [business for business in registered_businesses if business['business_id'] == business_id]
        # check if business exists
        if my_business:
            # check if user owns the business
            if my_business[0]['business_owner'] == business_owner:
                if 'business_name' in test_business:
                    my_business[0]['business_name'] = test_business['business_name']
                if 'business_location' in test_business:
                    my_business[0]['business_location'] = test_business['business_location']
                if 'business_category' in test_business:
                    my_business[0]['business_category'] = test_business['business_category']
                if 'email' in test_business:
                    my_business[0]['email'] = test_business['email']
                if 'contact_number' in test_business:
                    my_business[0]['contact_number'] = test_business['contact_number']
                return {'message': 'Business updated successfully'}, 201
            else:
                return {"message": "Not enough privileges to perform action"}, 200
        else:
            return {"message": "Business does not exist"}, 200

    @staticmethod
    def delete_registered_business(business_owner,business_id, registered_businesses):
        """ method allows a user to delete a business they registered"""
        my_business = [business for business in registered_businesses if business['business_id'] == business_id]
        # check if business exists
        if my_business:
            # check for ownership
            if my_business[0]['business_owner'] == business_owner:
                registered_businesses.remove(my_business[0])
                return {"message": "Business has been deleted successfully"}, 200
            else:
                return {"message": "Not enough privileges to perform action"}, 200
        else:
            return {"message": "Business not found"}, 200

    @staticmethod
    def get_all_businesses(businesses):
        return businesses

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False
