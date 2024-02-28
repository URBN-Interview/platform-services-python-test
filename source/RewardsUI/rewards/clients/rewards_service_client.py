import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://localhost:7050/rewards"
        self.user_url = "http://localhost:7050/rewards/users"
        self.order_url = "http://localhost:7050/rewards/order"

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

