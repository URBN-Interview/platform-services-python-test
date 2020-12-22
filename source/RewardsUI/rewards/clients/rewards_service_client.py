import requests


class RewardsServiceClient:

    def __init__(self):
        self.base_url = "http://rewardsservice:7050"
        self.rewards_url = self.base_url + "/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def post_rewards(self, email_address, amount):
        response = requests.post(self.rewards_url,
                                 params={"email_address": email_address, "amount": amount})
        return response.json()


class CustomerRewardsClient:

    def __init__(self):
        self.customer_rewards_url = "http://rewardsservice:7050/rewards/customers"

    def get_customers(self, email_address):
        response = requests.get(self.customer_rewards_url, params={"email_address": email_address})
        return response.json()
