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
            return {"business_name": "Not found", "review": "None"}

    @staticmethod
    def add_review(review):
        """ method allows a user to add a review to a registered business"""
        # check if the business to add the review to exists
        response = {'review_id': review.review_id,
                    'review': review.review,
                    'business_id': review.business_id,
                    }
        return response
