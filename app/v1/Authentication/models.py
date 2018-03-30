from flask import jsonify, request, make_response
from app.v1 import app
import jwt, datetime
import re


class User(object):
    """User class"""
    def __init__(self, user_id, username, password, first_name, last_name, email, gender, login_status):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.login_status = login_status

    def __str__(self):
        return "User(user_id='%s')" % self.user_id

    @staticmethod
    def register(new_user):
        """Register a user"""
        message = 'User registered successfully'
        response = {
            'user_id': new_user.user_id,
            'username': new_user.username,
            'password': new_user.password,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'gender': new_user.gender,
            'login_status': new_user.login_status,
        }
        return response

    @staticmethod
    def is_valid_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        else:
            return False

    @staticmethod
    def is_valid_gender(gender):
        if re.match(r"(^(?:m|M|male|Male|f|F|female|Female)$)", gender):
            return True
        else:
            return False

    @staticmethod
    def logout(current_user, registered_users):
        """Logs out a user"""
        my_user = [user for user in registered_users if user['username'] == current_user]
        if my_user:
            if my_user[0]['login_status'] is True:
                my_user[0]['login_status']= False
                message = 'You have successfully logged out'
                response = {'message': message}, 201
                return response
            else:
                return {'message': 'You are currently not logged in'}, 200
        else:
            return {'message': 'User not found'}, 200

    @staticmethod
    def login(username, password, registered_users):
        """Logs in a user"""
        # create mock-up data to authenticate the user
        #my_user = User(user_id='1', username='moses',password='banana', first_name='Moses', last_name ='Baguma',
        #              email='baguma@gmail.com', gender='male')
        my_user = [user for user in registered_users if user['username'] == username]
        if my_user:
            if my_user[0]['password'] == password:
                if my_user[0]["login_status"] is False :
                    token = jwt.encode({'username': username,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=40)},
                                   app.config['SECRET_KEY'])
                    my_user[0]['login_status'] = True
                    return {'token': token.decode('utf-8'), 'message': 'You have successfully logged in!.'
                                                            'Token created successfully'}, 201
                else:
                    return {'message': 'You are currently logged in'}, 200
            else:
                return {"message": "Invalid username or password"}, 200

        else:
            return {"message": "User not found"}

    @staticmethod
    def password_reset(current_user, new_password, registered_users):
        """reset user password"""
        # my_user = User(user_id=1, username='moses', password='banana', first_name='Moses', last_name='Baguma',
        #                email='baguma@gmail.com', gender='male')
        my_user = [user for user in registered_users if user['username'] == current_user]
        if my_user:
            if my_user[0]['login_status'] is True:
                my_user[0]['password'] = new_password
                message = "Password has been successfully reset"
                return {'message': message}, 201
            else:
                return {'message': 'You are not currently logged in to perform this action'}, 200
        else:
            return {'message': 'User not found'}, 200


