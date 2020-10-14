# Objective
* Using the [Django](https://www.djangoproject.com/) Python web framework, create a Customer Rewards Dashboard that calls the RESTful endpoints created in [RewardsService](https://github.com/urbn/platform-services-python-test/tree/init/source/RewardsService).

# Instructions:
* Modify the [incomplete dashboard](https://github.com/urbn/platform-services-python-test/blob/init/source/RewardsUI/rewards/index.html) to add the following features:
    * **Add Orders** section:
        * Submit a customer's order data
    * **User Rewards** section:
        * Display a table of the rewards data of all customers
        * Filter the table for a specific customer
* For bonus points, add CSS and error handling.

# Setup
* Install docker and docker-compose dependencies.
* $ cd APP_PATH/platform-services-python-test/source/RewardsUI
* $ docker-compose build
* $ docker-compose up -d
* Open http://localhost:8000/rewards/ in your browser.
