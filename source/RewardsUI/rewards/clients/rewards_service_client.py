import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.submit_url = "http://rewardsservice:7050/endpoint1"
        self.allusers_url = "http://rewardsservice:7050/endpoint3"
        self.user_url = "http://rewardsservice:7050/endpoint2"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def submit_order(self, email, amount):
        response = requests.get(self.submit_url, {'email': email, 'amount':amount})
        return response

    def get_allusers(self):
        response = requests.get(self.allusers_url)
        return response.json()

    def get_user(self, email):
        response = requests.get(self.user_url, {'email': email})
        return response.json()

