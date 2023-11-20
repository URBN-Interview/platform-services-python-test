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

# Implementation
* **RewardsView Class:**
    * Fetches rewards a user can earn and displays all customers' rewards data.
    * Utilizes the RewardsServiceClient to communicate with the RewardsService.
* **CustomerRewardsView Class:**
    * Retrieves either customer-specific rewards data based on the provided email or displays rewards data for all customers.
    * Utilizes the RewardsServiceClient to communicate with the RewardsService.
* **CustomerOrderView Class:**
    * Handles the submission of customer orders via the RewardsService by calling the submit_order method in RewardsServiceClient.
* **RewardsServiceClient Class:**
    * Communicates with the RewardsService's RESTful endpoints (rewards, order/rewards, user/rewards, allcustomers/rewards) using the requests library.
    * Provides methods to fetch rewards, submit orders, and retrieve customer-specific or all customers' rewards data.
* The interactions are based on RESTful API calls to the RewardsService endpoints, enabling the RewardsUI to display rewards data and submit new orders efficiently.

# Services
* Web application services are accessible at http://localhost:8000/
* Connects to external rewardsservice container from the RewardsService for interaction between the UI and the service. Uses default and rewardsservice_default networks for communication.

