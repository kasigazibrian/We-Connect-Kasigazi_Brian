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
        return "Business(user_id='%s')" % self.user_id


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
        return "Business(business_id='%s')" % self.business_id


class Register(object):
    """Signup class for registering a new user"""
    def __init__(self, new_user_id, first_name, last_name, username, password,
                 email, gender, message):
        self.new_user_id = new_user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.message = message

    def __str__(self):
        return "Signup(id='%s')" % self.new_user_id


class Reviews(object):
    """Reviews class for creating a review"""
    def __init__(self, review_id, business_id, review, message):
        self.review_id = review_id
        self.review = review
        self.business_id = business_id
        self.message = message

    def __str__(self):
        return "Reviews(id='%s')" % self.review_id
