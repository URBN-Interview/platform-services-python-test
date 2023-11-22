import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.order_url = "http://rewardsservice:7050/add-order"
        self.customers_url = "http://rewardsservice:7050/get-customers"
        self.customer_filter_url = "http://rewardsservice:7050/get-customer-data"

    def get_rewards(self):
        # gets the rewards collection using the rewards endpoint and returns the response
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        # gets the customers collection using the get-customers endpoint and returns the response
        response = requests.get(self.customers_url)
        return response.json()

    def get_filtered_customer(self, email):
        # gets the datapoints in the customers collection that match the given email and return the response
        # uses the get-customer-data endpoint
        response = requests.get(self.customer_filter_url + "?email=" + email)
        return response.json()

    def add_order(self, email, order_total):
        # calls add-order using the given email and order total. Should populate/update the appropriate datapoint
        requests.post(self.order_url + "?email=" + email + "&order-total=" + str(order_total))
