import requests
import json


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        try:
            response = requests.get(self.rewards_url)
            return response.json()
        except Exception as err:
            raise err
    
    # add_order
    # handler for submitting customer order info to API
    def add_order(self, order):
        try:
            response = requests.post(self.rewards_url, data=json.dumps(order))
            return response.json()
        except Exception as err:
            raise err
