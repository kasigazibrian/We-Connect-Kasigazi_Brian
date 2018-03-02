from app.models import db, Business
from app import app
from flask_testing import TestCase
import unittest, json


class BaseTestCase(TestCase):
    """Base test case to test the API"""
    def create_app(self):
        app.config['TESTING']= True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:brian@localhost/dbtests'
        return app

    def setUp(self):
        db.create_all()
        self.businesses =[{
            "business_name": "media studios",
            "business_category": "entertainment",
            "business_location": "kampala",
            "business_nominal_capital": "200000",
            "business_email": "supercom@gmail.com",

        },
            {
                "business_name": "real houses",
                "business_category": "real estate",
                "business_location": "kabale",
                "business_email": "real@gmail.com",
                "business_nominal_capital": "200000"

        }]
        business1 =Business(business_name=self.businesses[0]['business_name'],
                            business_location=self.businesses[0]['business_location'],
                            business_category=self.businesses[0]['business_category'],
                            business_email=self.businesses[0]['business_email'],
                            business_nominal_capital=self.businesses[0]['business_nominal_capital']
                            )
        business2 = Business(business_name=self.businesses[1]['business_name'],
                             business_location=self.businesses[1]['business_location'],
                             business_category=self.businesses[1]['business_category'],
                             business_email=self.businesses[1]['business_email'],
                             business_nominal_capital=self.businesses[1]['business_nominal_capital']
                             )
        db.session.add(business1)
        db.session.add(business2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    """Test class for business"""
    def test_API_can_create_a_business(self):
        """Tests if a business is created"""
        response = self.client.post("/api/v1/businesses", data=json.dumps(self.businesses[0]))
        self.assertIn('business created successfully', str(response.data))

    def test_API_can_obtain_a_specific_business(self):
        """Tests if one can retrieve a specific business"""
        tester = app.test_client(self)
        res = tester.post('/api/v1/businesses', data=json.dumps(self.businesses[0]))
        self.assertIn('business created successfully', str(res.data))
        res = tester.get('/api/v1/businesses/3')
        self.assertEqual(res.status_code, 200)
        self.assertIn('MyFi', str(res.data))

    def test_API_can_get_all_businesses(self):
        tester = app.test_client(self)
        res = tester.post('/api/v1/businesses', data=json.dumps(self.businesses[0]))
        self.assertIn('business created successfully', str(res.data))
        response = tester.get("/api/v1/businesses", data=json.dumps(self.businesses[0]))
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
        response = tester.post("/api/v1/businesses", data=json.dumps(self.businesses[0]))
        self.assertIn('business created successfully', str(response.data))
        result_in_json = json.loads(response.data.decode('utf-8').replace("'", "\""))
        res = tester.put('/api/v1/businesses/{}'.format(result_in_json['business_id']), data=json.dumps(self.businesses[0]))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Token is missing', str(res.data))

if __name__ == '__main__':
    unittest.main()