import json
import unittest
from app.models import db
from app.app import app
from flask_testing import TestCase
from werkzeug.security import generate_password_hash, check_password_hash


class BaseTestCase(TestCase):
    """Base test case to test the API"""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:brian@localhost/dbtests'
        return app

    def setUp(self):
        db.create_all()
        self.user = {
            "username": "martin",
            "password": "banana",
            "first_name": "Martin",
            "last_name": "Lawrence",
            "email": "martin@gmail.com",
            "gender": "male"
        }
        # hashed_password = generate_password_hash(self.user['password'], method='sha256')
        # new_user = User(username=self.user['username'], password=hashed_password, first_name=self.user['first_name'],
        #                 last_name=self.user['last_name'], email=self.user['email'], gender=self.user['gender'])
        # db.session.add(new_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
    def test_api_can_not_create_user_without_all_fields(self):
        """Tests if api will fail to create a user if all fields are not provided"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password":"mango", "first_name":"Moses"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('All fields are required, that is username, password, first_name, last_name,'
                      ' email and gender', str(response.data))

    def test_api_can_not_create_user_without_a_valid_email(self):
        """Tests if api will fail to create a user if the email provided is not valid"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses", "last_name":"Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Not a valid email address', str(response.data))

    def test_api_can_not_create_user_without_valid_gender(self):
        """Tests if api will fail to create a user if the email provided is not valid"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "e"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid gender. Try Male, Female, M, F', str(response.data))

    def test_API_can_create_a_user_account(self):
        """Tests if a user account is created"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))

    def test_API_can_not_create_a_user_account_twice(self):
        """Tests if a user account is created only once to show the username unique key constraint works"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('User already exists', str(response.data))

    def test_API_can_not_create_a_user_account_with_the_same_email(self):
        """Tests if a user account is created only once to show the email unique key constraint works"""
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        test_user = {"username": "micheal", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Email address already exists', str(response.data))

    def test_log_in_post_request_will_fail_without_all_required_credentials(self):
        """Tests if a user can be logged in"""
        # First add the user
        tester = app.test_client(self)
        with tester:
            test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                         "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
            response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
            self.assertEqual(response.status_code, 201)
            self.assertIn('User added successfully', str(response.data))
            user_login = {"username": "moses"}
            response = tester.post("/api/v2/login", data=json.dumps(user_login))
            self.assertEqual(response.status_code, 200)
            self.assertIn('Both username and password are required', str(response.data))

    def test_log_in_post_request_will_fail_with_invalid_credentials(self):
        """Tests if a user can be logged in"""
        # First add the user
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        user_login = {"username": 'moses', "password": "banana"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Your username or password is incorrect', str(response.data))

    def test_log_in_post_request(self):
        """Tests if a user can be logged in"""
        # First add the user
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))

    def test_user_will_not_be_able_to_login_twice(self):
        """Tests if a user can be logged in"""
        # First add the user
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        res = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(res.status_code, 201)
        self.assertIn('You are currently logged in.', str(res.data))

    def test_password_reset_post_request_will_fail_without_token(self):
        """Tests if password reset will fail without token"""
        new_password = {'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_logout_post_request_will_fail_without_token(self):
        """Tests if a user logs out"""
        response = self.client.post("/api/v2/auth/logout")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_password_can_be_reset_with_token(self):
        """Tests that password will be reset when the token is preent"""
        # First add the user
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        new_password = {'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password),
                                    headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Password has been reset successfully', str(response.data))

    def test_user_can_logout_with_token(self):
        """Tests that password will be reset when the token is preent"""
        # First add the user
        tester = app.test_client(self)
        test_user = {"username": "moses", "password": "mango", "first_name": "Moses",
                     "email": "moses@gmail.com", "last_name": "Lawrence", "gender": "male"}
        response = tester.post("/api/v2/auth/register", data=json.dumps(test_user))
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully', str(response.data))
        # Then log in the user
        user_login = {"username": 'moses', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user_login))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        new_password = {'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/logout", data=json.dumps(new_password),
                                    headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn('You have successfully logged out', str(response.data))


if __name__ == '__main__':
    unittest.main()
