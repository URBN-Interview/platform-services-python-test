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
