import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.orders_url = "http://rewardsservice:7050/order"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_order(self, email_address, order_total):
        order_data = {
            "email address": email_address,
            "order total": order_total
        }
        requests.post(self.orders_url, data=order_data)
