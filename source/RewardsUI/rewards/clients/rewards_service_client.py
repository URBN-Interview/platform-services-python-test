import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.user_rewards_url = "http://rewardsservice:7050/rewards_data"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    
    def get_user_rewards(self):
        response = requests.get(self.user_rewards_url)
        return response.json()

    def submit_order(self, form):
        response = requests.post(self.user_rewards_url, form)
        return response
