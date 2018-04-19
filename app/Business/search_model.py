from app.Business.models import Business


def search_by_name(business_name):
    """search for business based on its name"""
    business_search_result = Business.query.filter(Business.business_name.ilike("%{}%".format(business_name))).all()
    if business_search_result:
        registered_businesses = []
        for business in business_search_result:
            business_data = {}
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            registered_businesses.append(business_data)
        return {'Businesses': registered_businesses}, 200
    else:
        return {"message": "Business has not been found"}, 400


def search_by_category(business_category):
    """Search for business based on category"""
    business_search_result = Business.query.filter\
        (Business.business_category.ilike("%{}%".format(business_category))).all()
    if business_search_result:
        registered_businesses = []
        for business in business_search_result:
            business_data = {}
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            registered_businesses.append(business_data)
        return {'Businesses': registered_businesses}, 200
    else:
        return {"message": "Business has not been found"}, 400


def search_by_location(business_location):
    """search for business based on location"""
    business_search_result = Business.query.filter\
        (Business.business_location.ilike("%{}%".format(business_location))).all()
    if business_search_result:
        registered_businesses = []
        for business in business_search_result:
            business_data = {}
            business_data['business_id'] = business.business_id
            business_data['business_owner_id'] = business.business_owner_id
            business_data['business_name'] = business.business_name
            business_data['business_email'] = business.business_email
            business_data['business_location'] = business.business_location
            business_data['contact_number'] = business.contact_number
            business_data['business_category'] = business.business_category
            registered_businesses.append(business_data)
        return {'Businesses': registered_businesses}, 200
    else:
        return {"message": "Business has not been found"}, 400


def search_by_location_and_category(business_location, business_category):
    """search for business based on location and category"""
    business_search_result = Business.query.filter\
        (Business.business_location.ilike("%{}%".format(business_location)))
    if business_search_result:
        search_result = business_search_result.filter\
            (Business.business_category.ilike("%{}%".format(business_category))).all()
        if search_result:
            registered_businesses = []
            for business in search_result:
                business_data = {}
                business_data['business_id'] = business.business_id
                business_data['business_owner_id'] = business.business_owner_id
                business_data['business_name'] = business.business_name
                business_data['business_email'] = business.business_email
                business_data['business_location'] = business.business_location
                business_data['contact_number'] = business.contact_number
                business_data['business_category'] = business.business_category
                registered_businesses.append(business_data)
            return {'Businesses': registered_businesses}, 200
        else:
            return {"message": "Business has not been found"}, 400
    else:
        return {"message": "Business has not been found"}, 400


def search_by_category_and_limit(business_category, limit):
    """Search for business based on category"""
    business_search_result = Business.query.filter\
        (Business.business_category.ilike("%{}%".format(business_category)))
    if business_search_result:
        try:
            my_limit = int(limit)
            my_result = business_search_result.paginate(per_page=my_limit, page=1, error_out=True).items
            registered_businesses = []
            for business in my_result:
                business_data = {}
                business_data['business_id'] = business.business_id
                business_data['business_owner_id'] = business.business_owner_id
                business_data['business_name'] = business.business_name
                business_data['business_email'] = business.business_email
                business_data['business_location'] = business.business_location
                business_data['contact_number'] = business.contact_number
                business_data['business_category'] = business.business_category
                registered_businesses.append(business_data)
            return {'Businesses': registered_businesses}, 200
        except ValueError:
            return {"message": "Make sure the limit is a valid integer value"}, 400
    else:
        return {"message": "Business has not been found"}, 400


def search_by_location_and_limit(business_location, limit):
    """search for business based on location"""
    business_search_result = Business.query.filter\
        (Business.business_location.ilike("%{}%".format(business_location)))
    if business_search_result:
        try:
            my_limit = int(limit)
            my_result = business_search_result.paginate(page=1, per_page=my_limit, error_out=True).items
            registered_businesses = []
            for business in my_result:
                business_data = {}
                business_data['business_id'] = business.business_id
                business_data['business_owner_id'] = business.business_owner_id
                business_data['business_name'] = business.business_name
                business_data['business_email'] = business.business_email
                business_data['business_location'] = business.business_location
                business_data['contact_number'] = business.contact_number
                business_data['business_category'] = business.business_category
                registered_businesses.append(business_data)
            return {'Businesses': registered_businesses}, 200
        except ValueError:
            return {"message": "Make sure the limit is a valid integer value"}, 400
    else:
        return {"message": "Business has not been found"}, 400


def search_by_location_and_category_and_limit(business_location, business_category, limit):
    """search for business based on location and category"""
    business_search_result = Business.query.filter\
        (Business.business_location.ilike("%{}%".format(business_location)))
    if business_search_result:
        search_result = business_search_result.filter\
            (Business.business_category.ilike("%{}%".format(business_category)))
        if search_result:
            try:
                my_limit = int(limit)
                my_result = search_result.paginate(per_page=my_limit, page=1, error_out=True).items
                registered_businesses = []
                for business in my_result:
                    business_data = {}
                    business_data['business_id'] = business.business_id
                    business_data['business_owner_id'] = business.business_owner_id
                    business_data['business_name'] = business.business_name
                    business_data['business_email'] = business.business_email
                    business_data['business_location'] = business.business_location
                    business_data['contact_number'] = business.contact_number
                    business_data['business_category'] = business.business_category
                    registered_businesses.append(business_data)
                return {'Businesses': registered_businesses}, 200
            except ValueError:
                return {'message': 'Make sure the limit is a valid integer value'}, 400
        else:
            return {"message": "Business has not been found"}, 400
    else:
        return {"message": "Business has not been found"}, 400


def search_by_limit(limit):
        """Get all businesses"""
        try:
            my_limit= int(limit)
            businesses = Business.query.paginate(per_page=my_limit, page=1, error_out=True).items
            if businesses:
                registered_businesses = []
                for business in businesses:
                    business_data = {}
                    business_data['business_id'] = business.business_id
                    business_data['business_owner_id'] = business.business_owner_id
                    business_data['business_name'] = business.business_name
                    business_data['business_email'] = business.business_email
                    business_data['business_location'] = business.business_location
                    business_data['contact_number'] = business.contact_number
                    business_data['business_category'] = business.business_category
                    registered_businesses.append(business_data)
                return {'Businesses': registered_businesses}, 200
        except ValueError:
            return {"message": "Make sure the limit is a valid integer value"}, 400
