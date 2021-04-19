import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.order_url = "http://rewardsservice:7050/order"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def add_order(self, email_address, order_total):
        response = requests.post(self.order_url, {"emailAddress": email_address, "orderTotal": order_total})
        return response
