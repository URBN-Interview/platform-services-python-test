import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.order_url = "http://rewardsservice:7050/manage_customer"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_order(self, email_address, order_total):
        response = requests.post(self.order_url, data={'email_address': email_address, 'order_total': order_total})
        return response.json()
