from app.v1 import app
from app.v1.Business.views import registered_businesses
from app.v1.Authentication.views import registered_users
import unittest
import json


class FlaskTestCase(unittest.TestCase):
    """This class represents the flask test cases"""
    def create_app(self):
        """Initialize the app"""
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """Define test variables and initialize app."""
        self.businesses =[ {
                'business_name': 'MyFi',
                'business_category': 'Information Technology',
                'business_location': 'kampala',
                'email': 'myfi@gmail.com',
                'contact_number': '256781712929'
            },
            {
            'business_name': 'Supercom',
            'business_category': 'Entertainment',
            'business_location': 'kampala',
            'email': 'supercom@gmail.com',
            'contact_number': '256781712929'
        }]
        self.user = [{
            'username': 'moses',
            'password': 'banana',
            'first_name': 'Moses',
            'last_name': 'Lawrence',
            'email': 'moses@gmail.com',
            'gender': 'male'

        },{
                'username': 'martin',
                'password': 'mango',
                'first_name': 'Martin',
                'last_name': 'Pierce',
                'email': 'martin@gmail.com',
                'gender': 'male'

            }]

    def tearDown(self):
        registered_businesses.clear()
        registered_users.clear()

    def test_API_can_not_create_a_business_without_all_fields(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        self.businesses[0]['business_name']= ""
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("All details are required to register a business",str(response.data))

    def test_API_can_not_create_a_business_without_a_valid_email(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        self.businesses[0]['email'] = "my_fi"
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid email address", str(response.data))

    def test_API_can_create_a_business(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] +
            " has been registered successfully",str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))

    def test_API_has_unique_business_name_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Business already exists",str(response.data))

    def test_API_has_unique_business_email_constraint(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        self.businesses[0]['business_name']= "my_business"
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Email already exists", str(response.data))

    def test_API_can_obtain_a_specific_business(self):
        """Tests if one can retrieve a specific business"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        my_id = {"id": 1}
        response = tester.get("/api/v1/businesses/{}".format(my_id['id']))
        self.assertEqual(response.status_code, 200)
        self.assertIn("MyFi",str(response.data))

    def test_API_can_get_all_businesses(self):
        """Tests if one can retrieve all registered businesses"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        response = tester.get("/api/v1/businesses")
        self.assertEqual(response.status_code, 200)
        self.assertIn("MyFi", str(response.data))
        self.assertIn("Supercom", str(response.data))

    def test_API_will_fail_to_delete_a_business_without_token(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        response = tester.delete("/api/v1/businesses/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_API_will_delete_a_business_with_token(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Delete business 1
        response = tester.delete("/api/v1/businesses/1", content_type="application/json",
                               headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status, '200 OK')
        self.assertIn("Business has been deleted successfully",str(response.data))

    def test_API_will_not_delete_a_business_without_owner(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        # add first test user
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0][
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        # log in user
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second test_user
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[1]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[1]['first_name'] + " " + self.user[1][
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'martin', "password": "mango"}
        # log in second user
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Delete business 1 using second users token
        response = tester.delete("/api/v1/businesses/1", content_type="application/json",
                                 headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status, '200 OK')
        self.assertIn("Not enough privileges to perform action", str(response.data))

    def test_Api_will_not_update_business_without_token(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        self.businesses[0]['business_name'] = "media_com"
        response = tester.put("/api/v1/businesses/1", data=json.dumps(self.businesses[0]),
                              content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_API_will_not_update_a_business_without_owner(self):
        """Tests if a business is deleted"""
        tester = app.test_client(self)
        # add first test user
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0][
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        # log in user
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second test_user
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[1]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[1]['first_name'] + " " + self.user[1][
                'last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'martin', "password": "mango"}
        # log in second user
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Update business 1 using second users token who does not own the business
        self.businesses[0]['business_name'] = "media_com"
        response = tester.put("/api/v1/businesses/1", data=json.dumps(self.businesses[0]),
                              content_type="application/json",
                              headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status, '200 OK')
        self.assertIn("Not enough privileges to perform action", str(response.data))

    def test_API_will_update_business_with_token(self):
        """Tests if a business is updated"""
        tester = app.test_client(self)
        res = tester.post("/api/v1/auth/register", data=json.dumps(self.user[0]), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            "User " + self.user[0]['first_name'] + " " + self.user[0]['last_name'] + " has been registered successfully",
            str(res.data))
        new_user = {"username": 'moses', "password": "banana"}
        response = tester.post("/api/v1/login", data=json.dumps(new_user), content_type="application/json")
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully logged in!.Token created successfully', str(response.data))
        # Add first business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[0]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Add second business
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[1]),
                               content_type="application/json", headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Business " + self.businesses[1]["business_name"] + " has been registered successfully",
                      str(response.data))
        # Edit business 1
        self.businesses[0]['business_name'] = "media_com"
        response = tester.put("/api/v1/businesses/1", data=json.dumps(self.businesses[0]), content_type="application/json",
                                 headers={"access-token": result_in_json["token"]})
        self.assertEqual(response.status, '201 CREATED')
        self.assertIn("Business updated successfully", str(response.data))


if __name__ == '__main__':
    unittest.main()