import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.submit_url = "http://rewardsservice:7050/endpoint1"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def submit_order(self, email, amount):
        response = requests.get(self.submit_url, {'email': email, 'amount':amount})
        return response
