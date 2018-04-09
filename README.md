# We-Connect-Kasigazi_Brian
Andela cohort vi extended bootcamp challenge

[![Build Status](https://travis-ci.org/kasigazibrian/We-Connect-Kasigazi_Brian.svg?branch=feature_challenge_2)](https://travis-ci.org/kasigazibrian/We-Connect-Kasigazi_Brian)

[![Coverage Status](https://coveralls.io/repos/github/kasigazibrian/We-Connect-Kasigazi_Brian/badge.svg?branch=feature_challenge_2)](https://coveralls.io/github/kasigazibrian/We-Connect-Kasigazi_Brian?branch=feature_challenge_2)
[![Coverage Status](https://coveralls.io/repos/github/kasigazibrian/We-Connect-Kasigazi_Brian/badge.svg?branch=feature_challenge_3)](https://coveralls.io/github/kasigazibrian/We-Connect-Kasigazi_Brian?branch=feature_challenge_3)

[![Maintainability](https://api.codeclimate.com/v1/badges/8cc3a4dcd5e37d903ad7/maintainability)](https://codeclimate.com/github/kasigazibrian/We-Connect-Kasigazi_Brian/maintainability)

## Description
WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability
to write reviews about the businesses they have interacted with.

---
### Pre-requisites
* [Python](https://docs.python.org/3/) version 3.6
* [PostgreSQL](https://www.postgresql.org/docs/current/static/tutorial.html)

## API endpoints

| API Endpoint | HTTP Method | Functionality | 
| :--- | :--- | :--- | 
| /api/auth/register | POST | Creates a user account |
| /api/auth/login | POST | Logs in a user | 
| /api/auth/logout | POST | Logs out a user|
| /api/auth/reset-password| POST | Password reset |
| /api/businesses| POST | Register a business|
| /api/businesses/```<businessId>``` | PUT | Updates a business profile|
| /api/businesses/```<businessId>``` | DELETE | Remove a business |
| /api/businesses | GET | Retrieves all businesses |
| /api/businesses/```<businessId>``` | GET | Get a business |
| /api/businesses/```<businessId>```/reviews | POST | Add a review for a business|
| /api/businesses/```<businessId>```/reviews | GET | Get all reviews for a business|


## Installation procedure
```
run the "pip install -r requirements.txt" to install all the dependencies
```

### Running the API
```
Run the "python runserver.py" command to run the API
```

##Setting up the databases and running migrations
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```
---
## Running the tests
```
$ py.test testsv2/test_user.py
$ py.test testsv2/test_business.py
$ py.test testsv2/test_review.py
```

---
## Author

*** 
Kasigazi Brian 
***

---