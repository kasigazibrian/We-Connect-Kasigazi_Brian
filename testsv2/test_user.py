import json
import unittest
from app.app import db, app
from flask_testing import TestCase


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

    def register(self):
        tester = app.test_client(self)
        response = tester.post("/api/v2/auth/register", data=json.dumps(self.user),
                                   content_type="application/json")
        return response

    def login(self):
        user = {"username": 'martin', "password": "banana"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        return response
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """This class represents the flask test cases"""
    def test_the_all_fields_constraint(self):
        """Tests if api will fail to create a user if all fields are not provided"""
        self.user['first_name'] = ""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 400)

    def test_for_valid_email(self):
        """Tests if api will fail to create a user if the email provided is not valid"""
        tester = app.test_client(self)
        self.user['email']= "martin"
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 400)

    def test_for_valid_gender(self):
        """Tests if api will fail to create a user if the email provided is not valid"""
        tester = app.test_client(self)
        self.user['gender'] = 'boy'
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 400)

    def test_creating_a_user_account(self):
        """Tests if a user account is created"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

    def test_username_availability(self):
        """Tests if a user account is created only once to show the username unique key constraint works"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        response = self.client.post("/api/v2/auth/register", data=json.dumps(self.user),content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_email_availability(self):
        """Tests if a user account is created only once to show the email unique key constraint works"""
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        self.user['username']= "moses"
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 400)

    def test_the_login_all_fields_constraint(self):
        """Tests if a user can be logged in"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        user = {"username": "moses"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_invalid_login(self):
        """Tests if a user can be logged in"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        user = {"username": 'martin', "password": "mango"}
        response = self.client.post("/api/v2/login", data=json.dumps(user), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        """Tests if a user can be logged in"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

    def test_double_login(self):
        """Tests if a user can be logged in"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        response =  BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        res = BaseTestCase.login(self)
        self.assertEqual(res.status_code, 401)

    def test_password_reset_token_required_constraint(self):
        """Tests if password reset will fail without token"""
        new_password = {'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_logout_will_fail_without_token(self):
        """Tests if a user logs out"""
        response = self.client.post("/api/v2/auth/logout")
        self.assertEqual(response.status_code, 401)

    def test_valid_password_reset(self):
        """Tests that password will be reset when the token is present"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        new_password = {'new_password': 'pineapple'}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password),
                                    headers={"access-token": json_result["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_password_reset_with_no_new_password(self):
        """Tests that password will be reset when the token is present"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        new_password = {'new_password': ''}
        response = self.client.post("/api/v2/auth/reset-password", data=json.dumps(new_password),
                                    headers={"access-token": json_result["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_valid_logout(self):
        """Tests that password will be reset when the token is present"""
        # First add the user
        response = BaseTestCase.register(self)
        self.assertEqual(response.status_code, 201)

        # Then log in the user
        response = BaseTestCase.login(self)
        self.assertEqual(response.status_code, 201)

        json_result = json.loads(response.data.decode('utf-8').replace("'", "\""))
        new_password = {'password': 'pineapple'}
        response = self.client.post("/api/v2/auth/logout", data=json.dumps(new_password),
                                    headers={"access-token": json_result["token"]}, content_type="application/json")
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
