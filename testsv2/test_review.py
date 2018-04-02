from flask_testing import TestCase
from app.app import app
from app.models import db
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
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
    def test_API_can_post_reviews(self):
        """Tests if a business review is added"""
        tester = app.test_client(self)
        # Add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business using the token after logging in
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.business),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.post("/api/v2/businesses/1/reviews", data=json.dumps(self.reviews[0]),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        # check for review added message
        self.assertIn('Review has been added successfully', str(response.data))

    def test_API_can_not_add_review_to_a_business_which_is_non_existent(self):
        """Tests if a review can be added to a non existent business"""
        tester = app.test_client(self)
        response = tester.post("/api/v2/businesses/1/reviews", data=json.dumps(self.reviews[0]),
                               content_type="application/json")
        self.assertEqual(response.status_code, 400)
        # check for review content
        self.assertIn("Business to add a review to does not exist. Please ensure "
                      "that you have indicated the correct business id", str(response.data))

    def test_API_can_get_all_reviews(self):
        """Tests if api can get all reviews"""
        tester = app.test_client(self)
        # Add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business using the token after logging in
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.business),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response= tester.post("/api/v2/businesses/1/reviews", data= json.dumps(self.reviews[0]),
                              content_type="application/json")
        self.assertIn('Review has been added successfully', str(response.data))
        response = tester.post("/api/v2/businesses/1/reviews", data=json.dumps(self.reviews[1]),
                               content_type="application/json")
        self.assertIn('Review has been added successfully', str(response.data))
        response = tester.post("/api/v2/businesses/1/reviews", data=json.dumps(self.reviews[2]),
                               content_type="application/json")
        self.assertIn('Review has been added successfully', str(response.data))
        response = tester.get("/api/v2/businesses/1/reviews")
        self.assertEqual(response.status_code, 200)
        self.assertIn('This business is awesome', str(response.data))
        self.assertIn('This business rocks', str(response.data))
        self.assertIn('They have poor customer care', str(response.data))


if __name__ == '__main__':
    unittest.main()
