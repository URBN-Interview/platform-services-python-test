import json
import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_rewards_url = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_order(self, payload):
        response = requests.post(self.customer_rewards_url, data=json.dumps(payload))
        return response.json()

    def get_customer_rewards(self, email=None):
        url = self.customer_rewards_url
        if email:
            url = url + "?email={}".format(email)
        response = requests.get(url)
        return response.json()
