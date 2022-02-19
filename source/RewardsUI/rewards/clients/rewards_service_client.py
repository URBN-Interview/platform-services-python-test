import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    
    # customer_order
    # handler for submitting customer order info to API
    def customer_order(self, order):
        response = requests.post(self.rewards_url, data=order)
        return response.json()
