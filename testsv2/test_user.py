
import json
import unittest
from app.models import db, User
from app import app
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash


class BaseTestCase(TestCase):
    """Base test case to test the API"""
    def create_app(self):
        app.config['TESTING']= True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:brian@localhost/dbtests'
        return app

    def setUp(self):
        db.create_all()
        self.user = {
            "username": "martin",
            "password": "banana",
            "first_name": "Martin",
            "last_name": "Lawrence",
            "email": "martin@gmail.com",
            "gender": "male"
        }
        hashed_password = generate_password_hash(self.user['password'], method='sha256')
        # new_user = User(username=self.user['username'], password=hashed_password, first_name=self.user['first_name'],
        #                 last_name=self.user['last_name'], email=self.user['email'], gender=self.user['gender'])
        # db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
    def test_API_can_create_a_user_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.user),headers={"Content-Type":"application/json"})
        # self.assertEqual(response.status_code, 201)
        #self.assertIn('User added successfully', str(response.data))

    def test_log_in_post_request(self):
        """Tests if a user is logged in"""
        new_user = {"username":'moses',"password":"banana"}
        response = self.client.post("/api/v2/login", data=json.dumps(new_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created successfully', str(response.data))
    
    def test_logout_post_request_will_fail_without_token(self):
        """Tests if a user logs out"""
        new_user = {"username": 'moses', "password": "banana"}
        response = self.client.post("/api/v2/auth/logout", data=json.dumps(new_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))
    
    def test_password_reset_post_request_will_fail_without_token(self):
        """Tests if the new password for a user is obtained"""
        # Test using user Moses and change his password from banana to oranges
        new_password ={'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))


if __name__ == '__main__':
    unittest.main()
