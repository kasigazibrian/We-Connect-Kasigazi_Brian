"""Business tests"""
from app.app import app, db
from flask_testing import TestCase
import unittest, json


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
        self.test_user2 = {"username": "mary", "password": "pineapple", "first_name":"Mary",
                           "last_name": "Sally", "email": "mary@gmail.com","gender": "female"}
        self.businesses = [{
            "business_name": "media studios",
            "business_category": "entertainment",
            "business_location": "kampala",
            "contact_number": "256781712929",
            "business_email": "supercom@gmail.com",
            "business_description": "This business gives the best wedding coverage"

        },
            {
                "business_name": "real houses",
                "business_category": "real estate",
                "business_location": "kabale",
                "business_email": "real@gmail.com",
                "contact_number": "256781712978",
                "business_description": "This business will get you the best house"

        }]

    def register(self):
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        return response

    def register2(self):
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user2),
                               content_type="application/json")
        return response

    def login(self):
        user = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        return response

    def login2(self):
        user = {"username": 'mary', "password": "pineapple"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        return response

    def register_business(self, json_result):
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        return response

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """Test class for business"""
    def test_business_registration_without_token(self):
        """Tests if a business is created"""
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_the_all_fields_required_constraint(self):
        """Tests if a business can be created without all the fields"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.businesses[0]['business_name'] = ""
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_business_registration(self):
        """Tests if a business is created"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_API_business_name_unique_constraint(self):
        """Tests if a business is created"""

        response =  BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)
        # Then log in the user

        response =  BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_business_email_unique_constraint(self):
        """Tests if a business is created"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        self.businesses[0]["business_name"] = "Wakanda"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_business_email(self):
        """Tests if a business is created"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        self.businesses[0]["business_name"]= "Wakanda"
        self.businesses[0]["business_email"] = "gmail"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_business_phone_number(self):
        """Tests if a business is created"""
        response =  BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        self.businesses[0]["business_name"] = "Uganda"
        self.businesses[0]["business_email"] = "wakanda@gmail.com"
        self.businesses[0]["contact_number"] = "cow"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_obtaining_a_specific_business(self):
        """Tests if one can retrieve a specific business"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses/1")
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json_result['Business']) == 1)

    def test_getting_business_with_invalid_business_id(self):
        """Tests if API can not retrieve a business which does not exist"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response =BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses/3")
        self.assertEqual(response.status_code, 400)

    def test_getting_all_businesses(self):
        """Tests if one can retrieve a specific business"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses")
        self.assertEqual(response.status_code, 200)

    def test_searching_businesses_by_name(self):
        """Tests if one can retrieve a specific business by name"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses?q=med")
        self.assertEqual(response.status_code, 200)

    def test_searching_businesses_with_invalid_name(self):
        """Tests if one can retrieve a specific business by name"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/api/v2/businesses?q=345")
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json_result["Businesses"]) == 0)

    def test_filtering_businesses_by_category(self):
        """Tests if one can filter businesses by category"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response= BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with category entertainment
        response = self.client.get("/api/v2/businesses?q=med&category=enter")
        self.assertEqual(response.status_code, 200)

    def test_filtering_businesses_with__invalid_category(self):
        """Tests if one can filter businesses with an invalid category"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response= BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with category entertainment
        response = self.client.get("/api/v2/businesses?q=med&category=45")
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(json_result["Businesses"]) == 0)

    def test_filtering_businesses_by_location(self):
        """Tests if one can filter businesses by location"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with location as kabale
        response = self.client.get("/api/v2/businesses?q=med&location=ka")
        self.assertEqual(response.status_code, 200)

    def test_filtering_businesses_by_location_and_category(self):
        """Tests if one can filter businesses by location and category"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with location as kabale
        response = self.client.get("/api/v2/businesses?q=real&location=kaba&category=real")
        self.assertEqual(response.status_code, 200)

    def test_filtering_businesses_by_location_and_category_and_limit(self):
        """Tests if one can filter businesses by location category and limit"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with location as kabale
        response = self.client.get("/api/v2/businesses?q=real&location=kaba&category=real&limit=1")
        self.assertEqual(response.status_code, 200)

    def test_filtering_businesses_with_invalid_location(self):
        """Tests if one can filter businesses with invalid location"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Retrieve business with location as kabale
        response = self.client.get("/api/v2/businesses?q=real&location=5867")
        self.assertEqual(response.status_code, 400)

    def test_number_of_results_per_page_limit(self):
        """Tests if one can retrieve a specific business by name"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Add the first business
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # Add the second business
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Get all the business but limit the number to one per page
        response = self.client.get("/api/v2/businesses?limit=1")
        self.assertEqual(response.status_code, 200)

    def test_limit_integer_constraint(self):
        """Tests if one can retrieve a specific business by name"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Add the first business
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # Add the second business
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # Get all the business but limit the number to one per page
        response = self.client.get("/api/v2/businesses?q=real&limit=rttr")
        self.assertEqual(response.status_code, 400)

    def test_deleting_business_without_token(self):
        """Tests if a business can be deleted without a token"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.delete("/api/v2/businesses/1")
        self.assertEqual(response.status_code, 401)

    def test_valid_business_deleting(self):
        """Tests if a business is deleted"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response = self.client.delete("/api/v2/businesses/1", headers={"access-token": json_result["Token"]},
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_business_ownership_constraint_on_deleting(self):
        """Tests if a business is deleted(to be modified)"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Add another test user Mary
        response = BaseTestCase.register2(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user moses
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        response =  BaseTestCase.login2(self)
        self.assertEqual(response.status_code, 201)

        # Get Mary's login token
        json_result= json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.delete("/api/v2/businesses/1", headers={"access-token": json_result["Token"]},
                                      content_type="application/json"
                                      )
        self.assertEqual(response.status_code, 401)

    def test_updating_business_without_token(self):
        """Tests if a business can be updated without a token"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # try to update business_name
        self.businesses[0]["business_name"]= "Toyota"
        response = self.client.put("/api/v2/businesses/1",  content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_updating_with_no_input(self):
        """Tests if a business can be updated with no field to update"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # try to update business_name
        business = {}
        response = self.client.put("/api/v2/businesses/1",
                                   data=json.dumps(business), headers={"access-token": json_result["Token"]},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_business_name__unique_constraint_on_update(self):
        """Tests if someone can update the business name with a name which is already available"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # Then register another business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # try to update business_name
        self.businesses[0]["business_name"] = "real houses"
        response = self.client.put("/api/v2/businesses/1",
                                   data=json.dumps(self.businesses[0]), headers={"access-token": json_result["Token"]},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_business_email__unique_constraint_on_update(self):
        """Tests if someone can update the business name with a name which is already available"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # Then register another business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

        # try to update business_name
        self.businesses[0]["business_email"] = "real@gmail.com"
        response = self.client.put("/api/v2/businesses/1",
                                   data=json.dumps(self.businesses[0]), headers={"access-token": json_result["Token"]},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_business_update(self):
        """Tests if a business can be updated with a token"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # try to update business_name
        self.businesses[0]["business_name"] = "Toyota"
        self.businesses[0]["business_email"] = "toyota@gmail.com"
        response = self.client.put("/api/v2/businesses/1",
                                   data=json.dumps(self.businesses[0]), headers={"access-token": json_result["Token"]},
                                   content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_invalid_business_update(self):
        """Tests if a business which does not exist can be updated"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)
        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        self.businesses[0]["business_name"] = "Toyota"
        response = self.client.put("/api/v2/businesses/2", data= json.dumps(self.businesses[0]),
                              headers={"access-token": json_result["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_business_ownership_constraint_on_updating(self):
        """tests if a user who does not own the business will fail to update it"""
        # add a test user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Add another test user
        response = BaseTestCase.register2(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the first user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)
        # get the token after logging in
        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))

        # Then register the business with user Moses as owner
        response = BaseTestCase.register_business(self, json_result)
        self.assertEqual(response.status_code, 201)

        # login the second user Mary who does not own the business
        response = BaseTestCase.login2(self)
        self.assertEqual(response.status_code, 201)

        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.businesses[0]["business_name"] = "Toyota"
        response = self.client.put("/api/v2/businesses/1", data=json.dumps(self.businesses[0]),
                              headers={"access-token": result_in_json["Token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
