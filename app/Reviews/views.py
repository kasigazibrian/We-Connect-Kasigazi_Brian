from flask import request, jsonify
from app import api
from app.Reviews.models import BusinessReviews
from flask_restful import Resource



sample_reviews = [{
    'review_id': '1',
    'business_id': '1',
    'review': 'This business is awesome',
},
    {
        'review_id': '2',
        'business_id': '1',
        'review': 'This business rocks',

    },
    {
        'review_id': '3',
        'business_id': '1',
        'review': 'They have poor customer care',

    }]


class Business_Reviews(Resource):
    """Class for business reviews"""
    def post(self,business_id):
        """Method for posting a business review"""
        test_review = request.get_json(force=True)
        business_id = test_review.get('business_id')
        review_id = test_review.get('review_id')
        review = test_review.get('review')
        new_review = BusinessReviews(review_id=review_id, business_id=business_id, review=review)
        response = BusinessReviews.add_review(new_review)
        all_reviews = sample_reviews.append(response)
        return jsonify(response)

    def get(self, business_id):
        """method for obtaining all the business reviews"""
        response = BusinessReviews.get_all_reviews(business_id=business_id, business_reviews=sample_reviews)
        return jsonify({'Reviews': response})


api.add_resource(Business_Reviews,'/api/businesses/<business_id>/reviews')
