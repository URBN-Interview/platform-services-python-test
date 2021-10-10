import json
import requests

from http import HTTPStatus

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_rewards_url = "http://rewardsservice:7050/customerrewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        if response.status_code == HTTPStatus.NO_CONTENT.value:
            return []
        else:
            return response.json()

    # Code to get the list of customer rewards
    def get_all_customer_rewards(self):
        response = requests.get(self.customer_rewards_url)
        if response.status_code == HTTPStatus.NO_CONTENT.value:
            return []
        else:
            return response.json()

    # Code to get the list of customer rewards
    def get_customer_rewards(self, email):
        query_params = {'email':email}
        response = requests.get(self.customer_rewards_url, params=query_params)
        if response.status_code == HTTPStatus.NO_CONTENT.value:
            return []
        else:
            return response.json()

    # Code to get the list of customer rewards
    def add_customer_rewards(self, email, orderTotal):
        data = {'email':email, 'orderTotal':orderTotal}
        headers = {'content-type': 'application/json'}
        response = requests.post(self.customer_rewards_url, data=json.dumps(data), headers=headers)
        if response.status_code == HTTPStatus.NO_CONTENT.value:
            return []
        else:
            return response.json()
