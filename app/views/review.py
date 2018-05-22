"""Views.py Reviews"""
from flask_restplus import Resource, fields
from app import api
from app.models.business import Business
from app.models.review import BusinessReviews

review_model = api.model('Review', {'review': fields.String('Business Review')})

review_out_model = api.model('Review_out', {'review': fields.String('Business review'),
                                            'business_id': fields.String('Business ID'),
                                            'date_created': fields.DateTime(dt_format='rfc822')})


class BusinessReviewsOperations(Resource):
    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    def get(self,business_id):
        """Method to get all business reviews"""
        reviews = BusinessReviews.get_all_reviews(business_id=business_id)
        return reviews

    @api.doc(responses={400: 'Bad Request', 200: 'Success', 201: 'Created', 401: 'Unauthorised', 500: 'Database Error'})
    @api.expect(review_model)
    def post(self, business_id):
        """Method to add a business review"""
        review = api.payload
        review = review.get('review')
        if not review:
            return {"Message": "No Review has been added, Please add a review", "Status": "Fail"}, 200
        business = Business.query.filter_by(business_id=business_id).first()
        if not business:
            return {"Message": "Business to add a review to does not exist. Please ensure"
                               " that you have indicated the correct business id", "Status": "Fail"}, 400
        review = BusinessReviews(review=review, business_id=business_id)
        add_business_review = BusinessReviews.add_review(review)
        return add_business_review


api.add_resource(BusinessReviewsOperations, '/api/v2/businesses/<business_id>/reviews')

