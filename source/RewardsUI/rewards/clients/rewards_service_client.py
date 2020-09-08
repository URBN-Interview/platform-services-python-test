import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

class CustomerServiceClient:

    def __init__(self):
        self.customer_url = "http://rewardsservice:7050/customer/(.*)"

    def get_customer(self, keys):
        response = requests.get(self.customer_url)
        return response.json()

class OrderServiceClient:

    def __init__(self):
        self.customer_url = "http://rewardsservice:7050/order/(.*)"

    