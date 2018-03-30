
from app.v1 import app
import unittest
import json
from app.v1.Authentication.views import registered_users


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

    def tearDown(self):
        """Tear down the application"""
        registered_users.clear()

    def test_API_welcome_page(self):
        """Tests if the home route is functional"""
        tester = app.test_client(self)
        res = tester.get("/home")
        self.assertEqual(res.status_code, 200)
        self.assertIn('You are welcome', str(res.data))

    def test_API_will_fail_to_create_a_user_account_without_all_fields(self):
        """Tests if a user account will not be created without all fields"""
        tester = app.test_client(self)
        self.user['password'] = ""
        with tester:
            res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
            self.assertEqual(res.status_code, 200)
            self.assertIn('All fields are required', str(res.data))

    def test_API_will_fail_to_create_a_user_account_without_valid_email(self):
        """Tests if a user account will not be created without a valid email"""
        tester = app.test_client(self)
        self.user['email']= "moses"
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Invalid email address', str(res.data))

    def test_API_will_fail_to_create_a_user_account_without_valid_gender(self):
        """Tests if a user account will be created without valid gender"""
        tester = app.test_client(self)
        self.user['gender']= "gty"
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn('Invalid gender, Try Female, Male, F, M', str(res.data))

    def test_API_will_create_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("User "+self.user['first_name']+" "+self.user['last_name']+" has been registered successfully",
                      str(res.data))

    def test_API_has_unique_username_constraint(self):
        """Tests if the API has a unique username constraint"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("User already exists", str(res.data))

    def test_API_has_unique_email_constraint(self):
        """Tests if the API has a unique email constraint"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        self.user['username'] = "Martin"
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Email already exists", str(res.data))

    def test_login_post_request_will_fail_without_a_registered_user(self):
        """Tests if login post request will work without correct username or password"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'mose', "password": self.user['password']}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('User not found', str(response.data))

    def test_login_post_request_will_fail_without_correct_information(self):
        """Tests if login post request will work without correct username or password"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "mango"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password', str(response.data))

    def test_log_in_post_request(self):
        """Tests if a user is logged in"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username":'moses',"password":"banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))

    def test_user_can_not_log_in_twice(self):
        """Tests if a user is not allowed to log in twice"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('You are currently logged in', str(response.data))

    def test_password_reset_post_request_will_fail_without_token(self):
        """Tests if the password for a user is updated without token"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Test using user Moses and change his password from banana to oranges
        new_password ={'new_password': 'oranges'}
        response = tester.post("/api/v1/auth/reset-password", data=json.dumps(new_password),
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_password_reset_post_request_will_work_with_token(self):
        """Tests if the password for a user is updated without token"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Test using user Moses and change his password from banana to oranges
        new_password = {'new_password': 'oranges'}
        response = tester.post("/api/v1/auth/reset-password", data=json.dumps(new_password),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Password has been successfully reset', str(response.data))

    def test_api_logout_post_request_will_fail_without_token(self):
        """Tests if a user can logout without token"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Test using user Moses and change his password from banana to oranges
        response = tester.post("/api/v1/auth/logout",
                               content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_logout_post_request_will_work_with_token(self):
        """Tests if the password for a user is updated without token"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user['first_name'] + " " + self.user['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Test using user Moses and change his password from banana to oranges
        new_password = {'new_password': 'oranges'}
        response = tester.post("/api/v1/auth/logout", data=json.dumps(new_password),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged out', str(response.data))


if __name__ == '__main__':
    unittest.main()