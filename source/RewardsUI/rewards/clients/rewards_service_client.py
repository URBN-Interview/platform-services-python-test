import requests


class RewardsServiceClient:

    def __init__(self):
        self.url = "http://rewardsservice:7050/"
        self.rewards_endpoint = "rewards"
        self.all_customers_endpoint = "customers"
        self.get_customer_endpoint = "customer"

    def get_rewards(self):
        response = requests.get(self.url + self.rewards_endpoint)
        return response.json()

    def get_customers(self):
        response = requests.get(self.url + self.all_customers_endpoint)
        return response.json()

    def get_customer(self, email):
        response = requests.get(self.url + self.get_customer_endpoint, {"email": email})
        return response.json()
