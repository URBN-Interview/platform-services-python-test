import requests


class RewardsServiceClient:

    def __init__(self):
        self.url = "http://rewardsservice:7050/orders"

    def get_order(self):
        response = requests.get(self.url)
        return response.json()
