from app.app import db


class BusinessReviews(db.Model):
    """Class model for business reviews"""
    review_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.business_id'))
    review = db.Column(db.VARCHAR(400))

    def __init__(self, business_id, review):
        self.business_id = business_id
        self.review = review

    @staticmethod
    def add_review(review_data):
        try:
            db.session.add(review_data)
            db.session.commit()
            return {'message': 'Review has been added successfully', "status": "Success"}, 201
        except:
            db.session.rollback()
            return {'message': 'An error occurred. Please contact administrator ', "status": "Fail"}, 500

    @staticmethod
    def get_all_reviews( business_id):
        all_reviews = BusinessReviews.query.filter_by(business_id=business_id).all()
        if all_reviews:
            reviews_added = []
            for my_review in all_reviews:
                review_data = {}
                review_data['business_id'] = my_review.business_id
                review_data['review'] = my_review.review
                reviews_added.append(review_data)
            return {'Businesses': reviews_added, "status": "Success"}, 200
        else:
            return {'message': 'No business reviews have been added yet', "status": "Fail"}, 400
