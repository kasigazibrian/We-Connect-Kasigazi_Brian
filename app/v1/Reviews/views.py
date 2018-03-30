from app.v1 import api
from app.v1.Reviews.models import BusinessReviews
from flask_restplus import Resource, fields
from app.v1.Business.views import registered_businesses
reviews = []

review_model = api.model('Review', {'review': fields.String('Business Review')})

review_out_model = api.model('Review_out', {'review': fields.String('Business review'),
                                            'business_name': fields.String('Business Name')})


class MyBusinessReviews(Resource):
    """Class for business reviews"""
    @api.expect(review_model)
    def post(self, business_id):
        """Method for posting a business review"""
        test_review = api.payload
        review_id = len(reviews) + 1
        review = test_review['review']
        my_business = [business for business in registered_businesses if business['business_id'] == business_id]
        if my_business:
            new_review = BusinessReviews(review_id=review_id, business_id=business_id, review=review)
            response = BusinessReviews.add_review(review= new_review)
            response['business_name'] = my_business[0]['business_name']
            reviews.append(response)
            return {"message": "Business review has been added successfully"}, 201
        else:
            return {"message": "Business to add a review to not found"}, 200

    @api.marshal_with(review_out_model, envelope="Reviews")
    def get(self, business_id):
        """method for obtaining all the business reviews"""
        response = BusinessReviews.get_all_reviews(business_id=business_id, business_reviews=reviews)
        return response, 200


api.add_resource(MyBusinessReviews,'/api/businesses/<int:business_id>/reviews')
