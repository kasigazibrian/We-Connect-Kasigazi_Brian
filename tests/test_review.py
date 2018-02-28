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
        self.review = { 'review':'4',
                        'business_id': '1',
                        'review': 'This business is the best'
                        }


    def test_API_can_post_reviews(self):
        """Tests if a business review is added"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.review))
        # check for review content
        self.assertIn('This business is the best', str(response.data))


    def test_API_can_get_all_reviews(self):
        """Tests if api can get all reviews"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.review))
        # check for review content
        self.assertIn('This business is the best', str(response.data))
        response = tester.get("/api/businesses/1/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertIn('This business is awesome', str(response.data))
        self.assertIn('This business rocks', str(response.data))
        self.assertIn('They have poor customer care', str(response.data))
        self.assertIn('This business is the best', str(response.data))


if __name__ == '__main__':
    unittest.main()