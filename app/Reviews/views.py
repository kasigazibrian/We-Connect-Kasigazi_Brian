"""Views.py Reviews"""
from flask_restplus import Resource, fields
from app.app import api
from app.Business.models import Business
from app.Reviews.models import BusinessReviews

review_model = api.model('Review', {'review': fields.String('Business Review')})

review_out_model = api.model('Review_out', {'review': fields.String('Business review'),
                                            'business_id': fields.String('Business ID')})


class BusinessReviewsOperations(Resource):
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    def get(self,business_id):
        """Method to get all business reviews"""
        all_reviews = BusinessReviews.get_all_reviews(business_id=business_id)
        return all_reviews

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    @api.expect(review_model)
    def post(self, business_id):
        """Method to add a business review"""
        new_review_data = api.payload
        review = new_review_data.get('review')
        if review:
            my_business = Business.query.filter_by(business_id=business_id).first()
            if my_business:
                new_business_review = BusinessReviews(review=review, business_id=business_id)
                add_business_review = BusinessReviews.add_review(new_business_review)
                return add_business_review
            else:
                return {"message": "Business to add a review to does not exist. Please ensure"
                                   " that you have indicated the correct business id", "status": "Fail"}, 400
        else:
            return {"message": "No Review has been added", "status": "Fail"}, 400


api.add_resource(BusinessReviewsOperations, '/api/v2/businesses/<business_id>/reviews')

