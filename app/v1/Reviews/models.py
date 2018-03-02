"""Class for Business Reviews"""


class BusinessReviews(object):
    """Reviews class for creating a review"""
    def __init__(self, review_id, business_id, review):
        self.review_id = review_id
        self.review = review
        self.business_id = business_id

    def __str__(self):
        return "BusinessReviews(review_id='%s')" % self.review_id

    @staticmethod
    def get_all_reviews(business_id, business_reviews):
        """Get all the reviews"""
        # check if business has reviews
        my_reviews = [review for review in business_reviews if review['business_id'] == business_id]
        if my_reviews:
            return my_reviews
        else:
            return "Business reviews not found"

    @staticmethod
    def add_review(review):
        """ method allows a user to add a review to a registered business"""

        # check if the business that has the review exists
        sample_review = BusinessReviews(review_id=review.review_id, business_id=review.business_id, review=review.review)
        response = {'review_id': sample_review.review_id,
                    'review': sample_review.review,
                    'business_id': sample_review.business_id,
                    'message': 'Review has been added successfully'
                    }
        return response