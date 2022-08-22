import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.orders_url = "http://rewardsservice:7050/orders"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_orders(self):
        response = requests.get(self.orders_url)
        return response.json()
