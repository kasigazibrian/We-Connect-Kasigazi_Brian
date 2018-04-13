from app.app import app
from flask_testing import TestCase
from app.models import db, Business
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
        self.businesses =[{
            "business_name": "media studios",
            "business_category": "entertainment",
            "business_location": "kampala",
            "contact_number": "256781712929",
            "business_email": "supercom@gmail.com",

        },
            {
                "business_name": "real houses",
                "business_category": "real estate",
                "business_location": "kabale",
                "business_email": "real@gmail.com",
                "contact_number": "256781712978"

        }]
        # db.session.add(business1)
        # db.session.add(business2)
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """Test class for business"""
    def test_API_can_not_create_a_business_without_a_logged_in_user(self):
        """Tests if a business is created"""
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    content_type="application/json")
        self.assertIn('Token is missing', str(response.data))

    def test_API_can_not_create_a_business_without_all_the_fields(self):
        """Tests if a business can be created without all the fields"""
        tester = app.test_client(self)
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
        self.businesses[0]['business_name'] = ""
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("All fields are required, that is business_name, business_email,"
                      "business_location, business_nominal_capital and business_category", str(response.data))

    def test_API_can_create_a_business(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
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
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))

    def test_API_business_name_integrity_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
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
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Business already exists", str(response.data))

    def test_API_business_email_integrity_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
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
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        self.businesses[0]["business_name"] = "Wakanda"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Email already exists", str(response.data))

    def test_API_business_email_validation_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
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
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        self.businesses[0]["business_name"]= "Wakanda"
        self.businesses[0]["business_email"] = "gmail"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a valid email", str(response.data))

    def test_API_business_phone_number_validation_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
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
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        self.businesses[0]["business_name"] = "Wakanda"
        self.businesses[0]["business_email"] = "wakanda@gmail.com"
        self.businesses[0]["contact_number"] ="sdhgsh"
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Not a valid phone number. Ensure it has ten digits", str(response.data))

    def test_API_can_obtain_a_specific_business(self):
        """Tests if one can retrieve a specific business"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.get("/api/v2/businesses/1")
        self.assertIn('media studios', str(response.data))

    def test_API_can_obtain_a_specific_business_which_does_not_exist(self):
        """Tests if API can not retrieve a business which does not exist"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login),  content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.get("/api/v2/businesses/3")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Business does not exist', str(response.data))

    def test_API_can_get_all_businesses(self):
        """Tests if one can retrieve a specific business"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.get("/api/v2/businesses")
        self.assertIn('media studios', str(response.data))
        self.assertIn('real houses', str(response.data))

    def test_API_can_get_business_by_name(self):
        """Tests if one can retrieve a specific business by name"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.get("/api/v2/businesses?q=media studios")
        self.assertIn('media studios', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_API_can_filter_businesses_by_category(self):
        """Tests if one can filter businesses by category"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # Retrieve business with category entertainment
        response = tester.get("/api/v2/businesses?category=entertainment")
        self.assertIn('media studios', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_API_can_filter_businesses_by_location(self):
        """Tests if one can filter businesses by location"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # Retrieve business with location as kabale
        response = tester.get("/api/v2/businesses?location=kabale")
        self.assertIn('real houses', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_API_can_limit_number_of_results_per_page(self):
        """Tests if one can retrieve a specific business by name"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Add the first business
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # Add the second business
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[1]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # Get all the business but limit the number to one per page
        response = tester.get("/api/v2/businesses?limit=1")
        self.assertIn('media studios', str(response.data))
        self.assertIsNot('real houses', str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_API_can_not_delete_business_without_token(self):
        """Tests if a business can be deleted without a token"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.delete("/api/v2/businesses/1")
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))

    def test_API_will_delete_a_business_with_token(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        response = tester.delete("/api/v2/businesses/1", headers={"access-token": result_in_json["token"]},
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business has been deleted successfully', str(response.data))

    def test_user_can_not_delete_business_he_did_not_add(self):
        """Tests if a business is deleted(to be modified)"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Add another test user Mary
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user2),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user2['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user moses
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        user_login = {"username": 'mary', "password": "pineapple"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        response = tester.delete("/api/v2/businesses/2", headers={"access-token": result_in_json["token"]},
                                 content_type="application/json"
                                 )
        self.assertEqual(response.status_code, 200)
        self.assertIn('You do not have enough privileges to delete this business', str(response.data))

    def test_API_will_not_update_business_without_token(self):
        """Tests if a business can be updated without a token"""
        """Tests if a business can be deleted without a token"""
        tester = app.test_client(self)
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # try to update business_name
        self.businesses[0]["business_name"]= "Toyota"
        response = tester.put("/api/v2/businesses/1",  content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token is missing', str(response.data))

    def test_API_will_update_business_with_a_token(self):
        """Tests if a business can be updated with a token"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))

        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # try to update business_name
        self.businesses[0]["business_name"] = "Toyota"
        response = tester.put("/api/v2/businesses/1",
                              data=json.dumps(self.businesses[0]), headers={"access-token": result_in_json["token"]},
                              content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Business updated successfully', str(response.data))
        res = tester.get("/api/v2/businesses/1", content_type="application/json")
        # check for new business name
        self.assertIn('Toyota', str(res.data))

    def test_user_can_not_update_business_which_does_not_exist(self):
        """Tests if a business which does not exist can be updated"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        self.businesses[0]["business_name"] = "Toyota"
        response = tester.put("/api/v2/businesses/2", data= json.dumps(self.businesses[0]),
                              headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn('Business not found', str(response.data))

    def test_if_user_who_does_not_own_the_business_can_update_it(self):
        """tests if a user who does not own the business will fail to update it"""
        tester = app.test_client(self)
        # add a test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user['first_name'] + ' has been added successfully', str(response.data))
        # Add another test user
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.test_user2),
                               content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('User ' + self.test_user2['first_name'] + ' has been added successfully', str(response.data))
        # Then log in the first user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        # Then register the business with user Moses as owner
        response = self.client.post("/api/v2/businesses", data=json.dumps(self.businesses[0]),
                                    headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business has been registered successfully", str(response.data))
        # login the second user Mary who does not own the business
        user_login = {"username": 'mary', "password": "pineapple"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        # get the token after logging in
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.businesses[0]["business_name"] = "Toyota"
        response = tester.put("/api/v2/businesses/1", data=json.dumps(self.businesses[0]),
                              headers={"access-token": result_in_json["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Not enough privilege to perform action', str(response.data))


if __name__ == '__main__':
    unittest.main()
