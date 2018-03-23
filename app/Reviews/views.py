from flask import request, jsonify
from flask_restful import Resource
from app.app import  api
from app.models import BusinessReviews, Business


class GetAllBusinessReviews(Resource):
    def get(self,business_id):
        """get all business reviews"""
        all_reviews = BusinessReviews.get_all_reviews(business_id=business_id)
        return all_reviews


class AddBusinessReview(Resource):
    def post(self, business_id):
        new_review_data = request.get_json(force=True)
        review = new_review_data.get('review')
        mybusiness = Business.query.filter_by(business_id=business_id).first()
        if mybusiness:
            new_business_review = BusinessReviews(review=review, business_id=business_id)
            add_business_review = BusinessReviews.add_review(new_business_review)
            return add_business_review
        else:
            return jsonify({"message":"Business to add a review to does not exist. Please ensure"
                                      " that you have indicated the correct business id"})


api.add_resource(GetAllBusinessReviews,'/api/v2/businesses/<business_id>/reviews')
api.add_resource(AddBusinessReview,'/api/v2/businesses/<business_id>/reviews')