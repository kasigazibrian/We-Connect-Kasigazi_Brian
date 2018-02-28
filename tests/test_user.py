
from app.v1 import app
import unittest
import json, jwt


class FlaskTestCase(unittest.TestCase):
    """This class represents the flask test cases"""

    def create_app(self):
        """Initialize the app"""
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = app.test_client(self)
        self.user = {
            'user_id': '1',
            'username': 'moses',
            'password': 'banana',
            'first_name': 'Moses',
            'last_name': 'Baguma',
            'email': 'baguma@gmail.com',
            'gender': 'male'

        }

    def test_API_can_create_a_user_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.post("/api/v1/auth/register", data=json.dumps(self.user))
        with response as res:
            self.assertEqual(res.status_code, 201)
            self.assertIn('User has been registered successfully', str(res.data))

    def test_log_in_post_request(self):
        """Tests if a user is logged in"""
        tester = app.test_client(self)
        new_user = {"username":'moses',"password":"banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Token created successful', str(response.data))

    def test_logout_post_request_will_fail_without_token(self):
        """Tests if a user logs out"""
        tester = app.test_client(self)
        response = tester.post("/api/v1/auth/logout", data=json.dumps(self.user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_password_reset_post_request_will_fail_without_token(self):
        """Tests if the new password for a user is obtained"""
        tester = app.test_client(self)
        # Test using user Moses and change his password from banana to oranges
        new_password ={'password': 'pineapple'}
        response = tester.post("/api/v1/auth/reset-password", data=json.dumps(new_password))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))


if __name__ == '__main__':
    unittest.main()