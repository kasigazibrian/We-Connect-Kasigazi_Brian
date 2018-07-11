# We Connect


[![Build Status](https://travis-ci.org/kasigazibrian/We-Connect-Kasigazi_Brian.svg?branch=master)](https://travis-ci.org/kasigazibrian/We-Connect-Kasigazi_Brian)
[![Coverage Status](https://coveralls.io/repos/github/kasigazibrian/We-Connect-Kasigazi_Brian/badge.svg?branch=master)](https://coveralls.io/github/kasigazibrian/We-Connect-Kasigazi_Brian?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/8cc3a4dcd5e37d903ad7/maintainability)](https://codeclimate.com/github/kasigazibrian/We-Connect-Kasigazi_Brian/maintainability)

## Description
WeConnect provides a platform that brings businesses and individuals together.
This platform creates awareness for businesses and gives the users the ability
to write reviews about the businesses they have interacted with.

## Getting Started
* Clone the repository by running the command
```
  git clone https://github.com/kasigazibrian/We-Connect-Kasigazi_Brian.git -b feature_challenge_3
```
* Navigate to the root folder
```
cd We-Connect-Kasigazi_Brian

```
### Pre-requisites
* [Python](https://docs.python.org/3/) version 3.6
* [PostgreSQL](https://www.postgresql.org/docs/current/static/tutorial.html)

### Installation procedure
* Run the command below to install all the dependencies
```
 pip install -r requirements.txt
```
### Setting up the databases and running migrations
```
 python manage.py db init
 python manage.py db migrate
 python manage.py db upgrade
```
### Running the tests
* Run the command below to run the tests
```
$ pytest
```

### Running the API
* Run the command below to run the API
```
python runserver.py
```
* Find the API swagger documentation on the link below to access the different API endpoints
```
 http://localhost:5555/
```

## API endpoints and their functionality

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


### Built-With
* [Flask](http://flask.pocoo.org/docs/0.12/)
* [Flask-Sqalchemy](http://flask-sqlalchemy.pocoo.org/2.3/)

### Acknowledgements
I would like to express my deepest appreciation to all those who have provided me the possibility to work on this 
project.  A special gratitude I give to my learning facilitator , whose contribution in stimulating
suggestions and encouragement has  helped me to coordinate my project.

### Author
Kasigazi Brian 



