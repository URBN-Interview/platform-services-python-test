import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.get_url = "http://rewardsservice:7050/all"
        self.get_user_data_url = "http://rewardsservice:7050/get"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all(self):
        response = requests.get(self.get_url)
        return response.json()

    def get_user(self):
        response = requests.get(self.get_user_data_url)
        return response.json()
