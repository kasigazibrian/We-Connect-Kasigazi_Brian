"""tests.py"""
from app import app
import unittest
import json


class FlaskTestCase(unittest.TestCase):
    """This class represents the flask test cases"""

    def create_app(self):
        """Initialize the app"""
        app.config['TESTING'] = True
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.client = app.test_client(self)
        self.users = [{
            'user_id': '1',
            'username': 'moses',
            'password': 'banana',
            'message': '',
            'login_status': ''
        },
            {
                'user_id': '2',
                'username': 'Mabel',
                'password': 'oranges',
                'message': '',
                'login_status': ''
         }
        ]

        self.businesses = [{
            'business_id': '1',
            'business_owner_id': '1',
            'business_name': 'media studios',
            'business_category': 'entertainment',
            'business_location': 'kampala',
            'email': 'supercom@gmail.com',
            'contact_number': '256781712929'
        },
            {
                'business_id': '2',
                'business_owner_id': '2',
                'business_name': 'real houses',
                'business_category': 'real estate',
                'business_location': 'kabale',
                'email': 'real@gmail.com',
                'contact_number': '256781712928'
            },
        ]
        self.reviews =[{
            'review_id':'1',
            'business_id':'1',
            'review':'This business is awesome',
            'message': '',
        },
            {
                'review_id': '2',
                'business_id': '2',
                'review': 'This business rocks',
                'message': '',
        },
            {
                'review_id': '3',
                'business_id': '3',
                'review': 'They have poor customer care',
                'message': '',

            }]


    def test_API_can_create_a_user_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/register", data=json.dumps(self.users))
        with response as res:
            self.assertEqual(res.status_code, 201)
            self.assertIn('user created successfully', str(res.data))

    def test_log_in_post_request(self):
        """Tests if a user is logged in"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/login", data=json.dumps(self.users))
        self.assertEqual(response.status_code, 201)
        self.assertIn('true', str(response.data))

    def test_logout_post_request(self):
        """Tests if a user logs out"""
        tester = app.test_client(self)
        response = tester.post("/api/auth/logout", data=json.dumps(self.users))
        self.assertEqual(response.status_code, 200)
        self.assertIn('false', str(response.data))

    def test_password_reset_post_request(self):
        """Tests if the new password for a user is obtained"""
        tester = app.test_client(self)
        # Test using user Moses and change his password from banana to oranges
        response = tester.post("/api/auth/reset-password", data=json.dumps(self.users))
        self.assertEqual(response.status_code, 200)
        self.assertIn('oranges', str(response.data))

    def test_API_can_create_a_business(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses", data=json.dumps(self.businesses))
        self.assertEqual(response.status_code, 201)
        self.assertIn('business created successfully', str(response.data))

    def test_API_can_update_a_business(self):
        """Tests if a business is updated(to be modified)"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses", data=json.dumps(self.businesses))
        self.assertEqual(response.status_code, 201)
        self.assertIn('business created successfully', str(response.data))
        response = tester.put("/api/businesses/1", data=json.dumps(self.businesses))
        self.assertEqual(response.status_code, 200)

    # def test_API_can_delete_a_business(self):
    #     """Tests if a business is deleted(to be modified)"""
    #     tester = app.test_client(self)
    #     response = tester.delete("/api/businesses/<business_id>", data=json.dumps(self.businesses))
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('', str(response.data))

    def test_API_can_post_reviews(self):
        """Tests if a business review is added"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses/<business_id>/reviews", data=json.dumps(self.reviews))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review added successfully', str(response.data))


if __name__=='__main__':
    unittest.main()