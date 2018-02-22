"""Models.py"""


class User(object):
    """User class for logging in a new user"""
    def __init__(self, user_id, username, password, message, login_status):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.message = message
        self.login_status = login_status

    def __str__(self):
        return "User(user_id='%s')" % self.user_id

    def password_reset(self, new_password, old_password):
        self.password= new_password
        return "password has been reset"


class Business(object):
    """Business class for registering a new business"""
    def __init__(self, business_id, business_owner_id, business_name, business_location,
                 business_category, contact_number, email, message):
        self.business_id = business_id
        self.business_owner_id = business_owner_id
        self.business_name = business_name
        self.business_location = business_location
        self.business_category = business_category
        self.contact_number = contact_number
        self.email = email
        self.message = message

        def __str__(self):
            return "Business(business_owner_id='%s')" % self.business_owner_id

    def update_registered_business(self, business_id, new_business_id, business_owner_id, new_name):
        """ method allows a user update a registered business"""

        # check if user owns the business
        if business_owner_id in self.business.keys():

            if business_id == new_business_id:
                self.business_name = new_name
                return 'updated successfully'
            else:
                return "business does not exist!"

        else:
            return "Not enough privilege to do action"

    def delete_registered_business(self, business_owner_id, business_id):
        """ method allows a user delete a business they registered"""
        if business_id in self.business.keys():
            if business_owner_id in self.business.keys():
                del self.business[business_id]
            else:
                return "business does not exist"

            return self.business
        else:
            return "Not enough privileges to do action"


class Reviews(object):
    """Reviews class for creating a review"""
    def __init__(self, review_id, business_id, review, message):
        self.review_id = review_id
        self.review = review
        self.business_id = business_id
        self.message = message

    def __str__(self):
        return "Reviews(id='%s')" % self.review_id

    def add_review(self, review_id,business_id, review):
        """ method allows a user add a review to a registered business"""

        # check if business has the review
        if business_id in self.reviews.keys():

            if review_id == self.review_id:
                self.review = review
                return 'updated successfully'
            else:
                return "review does not exist!"

        else:
            return "Not enough privilege to do action"

    def delete_review (self, review_id, business_id):
        # check if business has the review
        if business_id in self.reviews.keys():

            # check if review exists
            if review_id == self.review_id:
                del review_id
                return 'deleted successfully'
            else:
                return "review does not exist!"

        else:
            return "Not enough privilege to do action"
