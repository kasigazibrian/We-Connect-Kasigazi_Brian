from flask_testing import TestCase
from app import app
from app.models import db, BusinessReviews
import unittest
import json


class BaseTestCase(TestCase):
    """Base test case to test the API"""
    def create_app(self):
        app.config['TESTING']= True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:brian@localhost/dbtests'
        return app

    def setUp(self):
        db.create_all()
        self.review = { "review": "This business is awesome"}
        new_review = BusinessReviews(review=self.review['review'])
        db.session.add(new_review)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
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