import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_reward(self, email):
        response = requests.get(self.rewards_url + '?email=' + email)
        return response.json()
