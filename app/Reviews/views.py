from flask import request
from flask_restful import Resource
from app import  api
from app.models import BusinessReviews


class GetAllBusinessReviews(Resource):
    def get(self,business_id):
        """get all business reviews"""
        all_reviews = BusinessReviews.get_all_reviews(business_id=business_id)
        return all_reviews


class AddBusinessReview(Resource):
    def post(self, business_id):
        new_review_data = request.get_json(force=True)
        review = new_review_data.get('review')
        new_business_review = BusinessReviews(review=review, business_id=business_id)
        add_business_review = BusinessReviews.add_review(new_business_review)
        return add_business_review


api.add_resource(GetAllBusinessReviews,'/api/v2/businesses/<business_id>/reviews')
api.add_resource(AddBusinessReview,'/api/v2/businesses/<business_id>/reviews')