import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.users_url = "http://rewardsservice:7050/allcustomers"
        self.order_url = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_user(self, email_address):
        response = requests.get(self.order_url, {"email-address": email_address})
        return response.json()

    def get_users(self):
        response = requests.get(self.users_url)
        return response.json()

    def add_order(self, email_address, order_total):
        response = requests.post(url=self.order_url, data={"email-address": email_address, "order-total": order_total})
        # return response.json()
