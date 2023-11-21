import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.order_url = "http://rewardsservice:7050/rewards-status"
        self.customers_url = "http://rewardsservice:7050/get-customers"
        self.customer_filter_url = "http://rewardsservice:7050/get-customer-data"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def get_filtered_customer(self, email):
        response = requests.get(self.customer_filter_url + "?email=" + email)
        return response.json()

    def add_order(self, email, order_total):
        requests.post(self.order_url + "?email=" + email + "&order-total=" + str(order_total))
