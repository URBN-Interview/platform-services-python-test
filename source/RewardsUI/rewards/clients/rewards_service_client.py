from urllib.parse import urljoin

import requests


class RewardsServiceClient:

    def __init__(self):
        self.base_url = "http://localhost:7050/"
        self.rewards_url = urljoin(base=self.base_url, url="rewards")
        self.user_url = urljoin(base=self.base_url, url="rewards/users")
        self.order_url = urljoin(base=self.base_url, url="rewards/order")

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_rewards(self, email_address, order_total):
        response = requests.post(self.order_url, json=dict(
            email_address=email_address,
            order_total=order_total
        ))
        return response.json()

    def get_users(self, email_address=""):
        response = requests.get(self.user_url, params=dict(email_address=email_address))
        return response.json()

