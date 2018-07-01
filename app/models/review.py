"""Reviews model"""
from app import db
from sqlalchemy import exc
import datetime


class BusinessReviews(db.Model):
    """Class model for business reviews"""
    review_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'))
    review = db.Column(db.VARCHAR(400))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, business_id, review):
        self.business_id = business_id
        self.review = review

    @staticmethod
    def add_review(review):
        try:
            db.session.add(review)
            db.session.commit()
            return {'Message': 'Review has been added successfully', "Status": "Success"}, 201
        except exc.DatabaseError:
            db.session.rollback()
            return {'Message': 'Database error. Please contact administrator ', 'Status': 'Fail'}, 500

    @staticmethod
    def get_all_reviews(business_id):
        all_reviews = BusinessReviews.query.filter_by(business_id=business_id).all()
        if not all_reviews:
            return {'Business Reviews': [], "Status": "Success"}, 400
        reviews_list = []
        for review in all_reviews:
            review_data = dict()
            dt = review.date_created.replace( microsecond=0)
            review_data['date_created'] = str(dt)
            review_data['business_id'] = review.business_id
            review_data['review'] = review.review
            reviews_list.append(review_data)
        # if len(reviews_list) == 1:
        #     return {'Business Review': reviews_list, "Status": "Success"}, 200
        return {'Business Reviews': reviews_list, "Status": "Success"}, 200
