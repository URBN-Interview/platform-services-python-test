import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.user_data_url = "http://rewardsservice:7050/endpoint_three"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_user_data(self):
        r = requests.get(self.user_data_url)
        return r.json()
