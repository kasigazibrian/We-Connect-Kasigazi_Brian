"""tests.py"""
from app import app
from flask import jsonify
import os
from app.models import User
import unittest
import json



class UserTestCase(unittest.TestCase):
    """This class represents the """

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = app.test_client(self)
        self.user = {
            'id': '1',
            'firstname': 'Moses',
            'lastname': 'Magezi',
            'email': 'moses@gmail.com',
            'username': 'moses',
            'password': 'banana',
            'gender': 'male'
        }
        self.login ={
            'id':'1',
            'username':'Mary',
            'password': '12345'
        }
        self.business = {
            'id': '1',
            'businessname': 'supercom',
            'businesslocategory': 'entertainment',
            'businesslocation': 'kampala',
            'email': 'supercom@gmail.com',
            'contactnumber': '256781712929'
        }




    def test_API_can_create_a_user_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/register", data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Moses', str(response.data))

    def test_log_in_post_request(self):
        """tests if a user is logged in(to be modified)"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mary', str(response.data))

    def test_logout_post_request(self):
        tester = app.test_client(self)
        response = tester.post("/api/auth/logout", data=self.login)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mary', str(response.data))

    def test_password_reset_post_request(self):
        tester = app.test_client(self)
        response = tester.post("/api/auth/reset-password", data=self.login)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mary', str(response.data))

    def test_API_can_create_a_business(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/register", data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Moses', str(response.data))

    def test_API_can_update_a_business(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.put("/api/businesses/<business_id>", data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Moses', str(response.data))

if __name__=='__main__':
    unittest.main()