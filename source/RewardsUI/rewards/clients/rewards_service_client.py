import requests

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://127.0.0.1:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
