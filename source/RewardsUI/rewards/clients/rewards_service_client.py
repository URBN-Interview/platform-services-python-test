import requests


class RewardsServiceClient:
    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_rewards_url = "http://rewardsservice:7050/customer-rewards"
        self.customer_orders_url = "http://rewardsservice:7050/orders"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customer_rewards(self, email=None):
        if email:
            response = requests.get(self.customer_rewards_url, params={'email': email})
            if response.ok:
                return [response.json()]
        else:
            response = requests.get(self.customer_rewards_url)
            if response.ok:
                return response.json()

        return []

    def add_customer_order(self, email, amount):
        requests.post(self.customer_orders_url, json={'email': email, 'amount': amount})
