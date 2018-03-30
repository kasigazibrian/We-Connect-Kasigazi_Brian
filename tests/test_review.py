from app.v1 import app
import unittest
import json
from app.v1.Authentication.views import registered_users
from app.v1.Business.views import registered_businesses
from app.v1.Reviews.views import reviews


class FlaskTestCase(unittest.TestCase):
    """This class represents the flask test cases"""

    def create_app(self):
        """Initialize the app"""
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.user = {
            'username': 'moses',
            'password': 'banana',
            'first_name': 'Moses',
            'last_name': 'Lawrence',
            'email': 'moses@gmail.com',
            'gender': 'male'

        }
        self.reviews = [{
                        'review': 'This business is the best'
                        },
                        {
                            'review': 'This business rocks'
                        },
                        {
                            'review': 'This business is awesome'
                        },]
        self.business = {
            'business_name': 'MyFi',
            'business_category': 'Information Technology',
            'business_location': 'kampala',
            'email': 'myfi@gmail.com',
            'contact_number': '256781712929'
        }

    def tearDown(self):
        registered_businesses.clear()
        registered_users.clear()
        reviews.clear()

    def test_API_can_not_post_reviews_to_a_non_existent_business(self):
        """Tests if a business review is added to a non existent business"""
        tester = app.test_client(self)
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.reviews[0]),
                               content_type="application/json")
        # check for response
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business to add a review to not found', str(response.data))

    def test_API_can_post_reviews(self):
        """Tests if a business review can be added"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user[
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.business),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.business["business_name"] + " has been registered successfully",
                      str(response.data))
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.reviews[0]),
                               content_type="application/json")
        # check for review content
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business review has been added successfully', str(response.data))

    def test_API_can_get_all_reviews(self):
        """Tests if api can get all reviews"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user[
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.business),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.business["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add the first review
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.reviews[0]),
                               content_type="application/json")
        # check for review 1 content
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business review has been added successfully', str(response.data))
        # Add second review
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.reviews[1]),
                               content_type="application/json")
        # check for review 2 content
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business review has been added successfully', str(response.data))
        # Add third review
        response = tester.post("/api/businesses/1/reviews", data=json.dumps(self.reviews[2]),
                               content_type="application/json")
        # check for review 3 content
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business review has been added successfully', str(response.data))
        # get all reviews
        res = tester.get("api/businesses/1/reviews", content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn('This business is the best', str(res.data))
        self.assertIn('This business rocks', str(res.data))
        self.assertIn('This business is awesome', str(res.data))

    def test_API_can_not_get_reviews_for_non_existent_businesses(self):
        """Tests if API can not get reviews for non existent businesses"""
        tester = app.test_client(self)
        response = tester.get("/api/businesses/1/reviews", content_type="application/json")
        # check for response
        self.assertEqual(response.status_code, 200)
        self.assertIn('Not found', str(response.data))


if __name__ == '__main__':
    unittest.main()