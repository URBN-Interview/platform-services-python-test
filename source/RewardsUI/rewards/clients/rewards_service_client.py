import requests


class RewardsServiceClient:

    def __init__(self):
        self.url = "http://rewardsservice:7050/"
        self.rewards_endpoint = "rewards"
        self.all_customers_endpoint = "customers"

    def get_rewards(self):
        response = requests.get(self.url + self.rewards_endpoint)
        return response.json()

    def get_customers(self):
        response = requests.get(self.url + self.all_customers_endpoint)
        return response.json()
