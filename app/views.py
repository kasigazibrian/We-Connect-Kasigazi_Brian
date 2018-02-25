"""views.py"""

from flask import request, jsonify
from app import app
from app.models import User, Business, Reviews


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    """route to home page"""
    return "success"


@app.route('/api/auth/register', methods=['POST'])
# creates user account
def register():
    test_users = request.get_json(force=True)
    test_user = test_users[0]
    user_id = test_user.get('user_id')
    username = test_user.get('username')
    password = test_user.get('password')
    login_status = test_user.get('login_status')
    if id and username and password:
        new_user = User(user_id=user_id, username=username, password=password,
                         message='', login_status=login_status)
        response = jsonify({
            'user_id': new_user.user_id,
            'username': new_user.username,
            'password': new_user.password,
            'login_status': new_user.login_status,
            'message': 'user created successfully'
        })
        response.status_code=201
        return response


@app.route('/api/auth/login', methods=['POST'])
# Logs in a user
def login():
    # obtain user data sent in a post request
    test_users = request.get_json(force=True)
    test_user = test_users[0]
    user_id = test_user.get('user_id')
    username = test_user.get('username')
    password = test_user.get('password')
    message = test_user.get('message')
    login_status = test_user.get('login_status')
    if user_id and username and password:
        new_user = User(user_id=user_id, username=username, password=password, message=message, login_status= login_status)
        # create test user to do authentication
        user = User(user_id='1', username='moses', password='banana', message='',login_status='')
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
    test_users = request.get_json(force=True)
    test_user = test_users[0]
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
    if request.method == 'POST':
        test_users = request.get_json(force=True)
        test_user = test_users[0]
        user_id = test_user.get('user_id')
        username = test_user.get('username')
        password = test_user.get('password')
        message =test_user.get('message')
        login_status =test_user.get('login_status')
        if id and username and password:
            new_user = User(user_id=user_id, username=username, password=password,
                              message='', login_status=login_status)
            # change the password to a new value
            response = jsonify({
                'new_user_id': new_user.user_id,
                'username': new_user.username,
                'password': 'oranges',
                'message': 'user created successfully',
                login_status: 'true'
            })

            return response


@app.route('/api/businesses', methods=['POST'])
#  Register a business
def businesses():
    if request.method == 'POST':
        test_businesses = request.get_json(force=True)
        test_business = test_businesses[0]
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
            response = jsonify({'message': 'No business data obtained'})
    else:
        response = jsonify({'message': 'Wrong Request'})
        return response


@app.route('/api/businesses/<int:business_id>', methods=['GET','POST','PUT','DELETE'])
# view specific business
def specific_business(business_id):
    if request.method=='GET':
        new_business = Business(business_id=1, business_name='alarm systems', business_owner_id=1,business_category='security',
                            contact_number='256781723456',business_location='kampala', email='deen@gmail.com', message='')
        business = new_business.get_specific_business(business_id)
        response = jsonify({
                'business_name': business
            })
        response.status_code = 200
        return response

    if request.method=='DELETE':
        new_business = Business(business_id=1, business_name='alarm systems', business_owner_id=1,
                                business_category='security',
                                contact_number='256781723456', business_location='kampala', email='deen@gmail.com',
                                message='')
        business = new_business.delete_registered_business(business_id=1, business_owner_id=1)
        response = jsonify({
            'message': business
        })
        response.status_code = 200
        return response

    if request.method == 'PUT':
        new_business = Business(business_id=1, business_name='alarm systems', business_owner_id=1,
                                business_category='security',
                                contact_number='256781723456', business_location='kampala', email='deen@gmail.com',
                                message='')
        business = new_business.update_registered_business(business_id=1, business_owner_id=1, new_name='mediacom')
        return business



@app.route('/api/businesses/<business_id>/reviews', methods=['GET', 'POST'])
def reviews(business_id):
    if request.method == 'GET':
       new_review = Reviews(review_id=1,business_id=business_id, review='Good job', message='my review')
       return jsonify({
           'review_id': new_review.review_id,
           'review': new_review.review,
           'business_id': new_review.business_id,
           'message': new_review.message
       })

    elif request.method=='POST':
        test_business_reviews = request.get_json(force=True)
        test_review = test_business_reviews[0]
        business_id = test_review.get('business_id')
        review_id = test_review.get('review_id')
        review = test_review.get('review')
        review_message =test_review.get('message')
        if review_id and business_id and review:
            sample_review = Reviews(review_id=review_id,business_id=business_id,review=review, message=review_message)
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

