from app import app
import unittest
import json, jwt


class FlaskTestCase(unittest.TestCase):
    """This class represents the flask test cases"""

    def create_app(self):
        """Initialize the app"""
        app.config['TESTING'] = True
        return app

    def setUp(self):
            """Define test variables and initialize app."""
            self.client = app.test_client(self)
            self.business = {
                'business_id': '3',
                'business_owner_id': '1',
                'business_name': 'MyFi',
                'business_category': 'Information Technology',
                'business_location': 'kampala',
                'email': 'myfi@gmail.com',
                'contact_number': '256781712929'
             }

    def test_API_can_create_a_business(self):
        """Tests if a business is created"""
        tester = app.test_client(self)
        response = tester.post("/api/v1/businesses", data=json.dumps(self.business))
        self.assertIn('business created successfully', str(response.data))

    def test_API_can_obtain_a_specific_business(self):
        """Tests if one can retrieve a specific business"""
        tester = app.test_client(self)
        res = tester.post('/api/v1/businesses', data=json.dumps(self.business))
        self.assertIn('business created successfully', str(res.data))
        res = tester.get('/api/v1/businesses/3')
        self.assertEqual(res.status_code, 200)
        self.assertIn('MyFi', str(res.data))

    def test_API_can_get_all_businesses(self):
        tester = app.test_client(self)
        res = tester.post('/api/v1/businesses', data=json.dumps(self.business))
        self.assertIn('business created successfully', str(res.data))
        response = tester.get("/api/v1/businesses", data=json.dumps(self.business))
        self.assertIn('media studios', str(response.data))
        self.assertIn('real houses', str(response.data))
        self.assertIn('MyFi', str(response.data))

    def test_API_will_fail_to_delete_a_business_without_token(self):
        """Tests if a business is deleted(to be modified)"""
        tester = app.test_client(self)
        response = tester.delete("/api/v1/businesses/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Token is missing', str(response.data))

    def test_API_will_not_update_business_without_token(self):
        """Tests if a business is updated(to be modified)"""
        tester = app.test_client(self)
        response = tester.post("/api/v1/businesses", data=json.dumps(self.business))
        self.assertIn('business created successfully', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        res = tester.put('/api/v1/businesses/{}'.format(result_in_json['business_id']), data=json.dumps(self.business))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Token is missing', str(res.data))



if __name__ == '__main__':
    unittest.main()