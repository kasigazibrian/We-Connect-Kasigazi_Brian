from flask import jsonify, request, make_response
from app.v1 import app
import jwt, datetime

class User(object):
    """User class"""
    def __init__(self, user_id, username, password, first_name, last_name, email, gender):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender

    def __str__(self):
        return "User(user_id='%s')" % self.user_id

    @staticmethod
    def register(new_user):
        """Register a user"""
        message = 'User registered successfully'
        response = jsonify({
            'user_id': new_user.user_id,
            'username': new_user.username,
            'password': new_user.password,
            'first_name': new_user.first_name,
            'last_name':new_user.last_name,
            'email': new_user.email,
            'gender': new_user.gender,
            'message': 'User has been registered successfully'
        })
        response.status_code = 201
        return response

    @staticmethod
    def logout(user_id):
        """Logs out a user"""
        my_user = User(user_id='1', username='moses', password='banana', first_name='Moses', last_name='Baguma',
                       email='baguma@gmail.com', gender='male')
        if user_id == my_user.user_id:
            message = 'You have successfully logged out'
            response = jsonify({'message': message})
            response.status_code = 200
            return response

    @staticmethod
    def login(username, password):
        """Logs in a user"""
        # create mock-up data to authenticate the user
        my_user = User(user_id='1', username='moses',password='banana', first_name='Moses', last_name ='Baguma',
                       email='baguma@gmail.com', gender='male')
        if username == my_user.username:
            if my_user.password == password:
                token = jwt.encode({'username': username,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40)},
                                    app.config['SECRET_KEY'])
                return jsonify({'token': token.decode('utf-8'),'message':'Token created successfully'})
            else:
                return make_response("could not verify", 401,
                                             {'WWW-Authenticate': 'Basic realm="Login required"'})
        else:
            return make_response("could not verify", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


    @staticmethod
    def password_reset(new_password):
        """reset user password"""
        my_user = User(user_id=1, username='moses', password='banana', first_name='Moses', last_name='Baguma',
                       email='baguma@gmail.com', gender='male')
        my_user.password = new_password
        message = "password has been reset"
        return jsonify({'new_password': new_password, 'message': message})