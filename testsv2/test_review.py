from flask_testing import TestCase
from app.app import db, app
import unittest
import json


class BaseTestCase(TestCase):
    """Base test case to test the API"""
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        self.test_user = {"username": "moses", "password": "mango",
                          "first_name": "Moses", "last_name": "Lawrence",
                          "email": "moses@gmail.com", "gender": "male"}
        self.business = {
            "business_name": "media studios",
            "business_category": "entertainment",
            "business_location": "kampala",
            "contact_number": "256781712927",
            "business_email": "supercom@gmail.com",

        }
        self.reviews = [{"review": "This business is awesome"}, {"review": "This business rocks"},
                       {"review": "They have poor customer care"}]

    def register(self):
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        return response

    def login(self):
        user = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        return response

    def register_business(self, json_result):
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.business),
                                    headers={"access-token": json_result["token"]}, content_type="application/json")
        return response

    def add_review(self, review):
        response = self.client.post("/api/v2/businesses/1/reviews", data=json.dumps(review),
                               content_type="application/json")
        return response

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
    def test_adding_review(self):
        """Tests if a business review is added"""
        # Add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business using the token after logging in
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.add_review(self, self.reviews[0])
        self.assertEqual(response.status_code, 201)

    def test_invalid_business(self):
        """Tests if a review can be added to a non existent business"""
        response = BaseTestCase.add_review(self, self.reviews[0])
        self.assertEqual(response.status_code, 400)

    def test_API_can_get_all_reviews(self):
        """Tests if api can get all reviews"""
        # Add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business using the token after logging in
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.add_review(self, self.reviews[0])
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.add_review(self, self.reviews[1])
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.add_review(self, self.reviews[2])
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses/1/reviews")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
