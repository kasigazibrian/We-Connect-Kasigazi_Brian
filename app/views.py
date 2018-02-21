"""views.py"""

from flask import request, jsonify
from app import app
from app.models import Signup, User, Business, Reviews


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    """route to home page"""
    return "success"


@app.route('/api/auth/register', methods=['POST'])
# creates user account
def register():
    test_user = request.get_json(force=True)
    new_user_id = test_user.get('new_user_id')
    username = test_user.get('username')
    password = test_user.get('password')
    first_name =test_user.get('first_name')
    last_name = test_user.get('last_name')
    email = test_user.get('email')
    gender = test_user.get('gender')
    if id and username and password and first_name and last_name and email and gender:
        new_user = Signup(new_user_id=new_user_id, username=username, password=password,
                          first_name=first_name, last_name=last_name, email=email, gender=gender, message='')
        response = jsonify({
            'new_user_id': new_user.new_user_id,
            'username': new_user.username,
            'password': new_user.password,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'gender': new_user.gender,
            'email': new_user.email,
            'message': 'user created successfully'
        })
        response.status_code=201
        return response


@app.route('/api/auth/login', methods=['POST'])
# Logs in a user
def login():
    # obtain user data sent in a post request
    test_user = request.get_json(force=True)
    user_id = test_user.get('user_id')
    username = test_user.get('username')
    password = test_user.get('password')
    message = test_user.get('message')
    login_status = test_user.get('login_status')
    if user_id and username and password:
        new_user = User(user_id=user_id, username=username, password=password, message=message, login_status=login_status)
        # create test user to do authentication
        user = User(user_id=1, username='Mary', password='12345', message='',login_status='')
        if(user.password == new_user.password) and (user.username == new_user.username):
            response = jsonify({
                'user_id': new_user.user_id,
                'username': new_user.username,
                'password': new_user.password,
                'message': 'logged in successfully',
                'login_status': 'true'

            })
            response.status_code = 201
            return response
        else:
            response = jsonify({'message': 'Invalid username or password'})
            return response
    else:
        response = jsonify({'message': 'No user data obtained'})
        return response


@app.route('/api/auth/logout', methods=['POST'])
# Logs out a user
def logout():
    # obtain user data sent in a post request
    test_user = request.get_json(force=True)
    user_id = test_user.get('user_id')
    username = test_user.get('username')
    password = test_user.get('password')
    message = test_user.get('message')
    login_status = test_user.get('login_status')
    if user_id and username and password:
        logged_in_user = User(user_id=user_id, username=username, password=password, message=message,
                        login_status=login_status)
        response =jsonify({
                           'user_id': logged_in_user.user_id,
                           'message': 'You have successfully logged out',
                           'login_status': 'false'
                           })
        return response
    else:
        response =jsonify({'message':'No user data obtained'})
        return  response


@app.route('/api/auth/reset-password', methods=['POST'])
# reset user password
def reset_password():
    if request.method=='POST':
        test_user = request.get_json(force=True)
        new_user_id = test_user.get('new_user_id')
        username = test_user.get('username')
        password = test_user.get('password')
        first_name = test_user.get('first_name')
        last_name = test_user.get('last_name')
        email = test_user.get('email')
        gender = test_user.get('gender')
        if id and username and password and first_name and last_name and email and gender:
            new_user = Signup(new_user_id=new_user_id, username=username, password=password,
                             first_name=first_name, last_name=last_name, email=email, gender=gender, message='')
            # change the password to a new value
            response = jsonify({
                'new_user_id': new_user.new_user_id,
                'username': new_user.username,
                'password': 'oranges',
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'gender': new_user.gender,
                'email': new_user.email,
                'message': 'user created successfully'
            })

            return response


@app.route('/api/businesses', methods=['POST'])
#  Register a business
def businesses():
    if request.method == 'POST':
        test_businesses = request.get_json(force=True)
        test_business=test_businesses[0]
        business_id = test_business.get('business_id')
        business_owner_id = test_business.get('business_owner_id')
        business_name = test_business.get('business_name')
        business_location= test_business.get('business_location')
        business_category= test_business.get('business_category')
        email = test_business.get('email')
        contact_number = test_business.get('contact_number')
        if business_id and business_owner_id and business_name and business_location and business_category\
                and email and contact_number:
            new_business = Business(business_id=business_id, business_owner_id=business_owner_id,
                                business_name=business_name, business_location=business_location,
                                business_category=business_category, email=email,
                                contact_number=contact_number, message='')
            # change the password to a new value
            response = jsonify({
                'business_id': new_business.business_id,
                'business_owner_id': new_business.business_owner_id,
                'business_name': new_business.business_name,
                'business_category': new_business.business_category,
                'first_name': new_business.email,
                'last_name': new_business.business_location,
                'email': new_business.contact_number,
                'message': 'business created successfully'
            })
            response.status_code=201
            return response
        else:
            response = jsonify({'message':'No business data obtained'})
    else:
        response= jsonify({'message':'Wrong Request'})
        return  response


@app.route('/api/businesses/<business_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
# view specific business
def specific_business(business_id):
    if request.method == 'GET':
        business = request.get_json()


    if request.method=='POST':
        pass
    if request.method=='DELETE':
        pass
    if request.method=='PUT':
        def update_business(business_id):
            businesses =request.get_json(force=True)
            # create test user who has same id as business owner moses which is 1

@app.route('/api/businesses/<business_id>/reviews', methods=['GET', 'POST'])
def reviews(business_id):
    if request.method=='GET':
        test_business_reviews = request.get_json(force=True)
        test_review =test_business_reviews[0]

    elif request.method=='POST':
        test_business_reviews = request.get_json(force=True)
        test_review = test_business_reviews[0]
        business_id = test_review.get('business_id')
        review_id = test_review.get('review_id')
        review = test_review.get('review')
        if review_id and business_id and review:
            sample_review = Reviews(review_id=review_id,business_id=business_id,review=review)
            response= jsonify({'review_id': sample_review.review_id,
                            'review' : sample_review.review,
                            'business_id': sample_review.business_id,
                            'message': 'Review added successfully'
                            })
            response.status_code = 201
            return response
        else:
            return 'No review data added'
    else:
        return 'wrong request'