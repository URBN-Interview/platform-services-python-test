import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.all_customers_url = "http://rewardsservice:7050/allcustomerpoints"
        self.single_customer_url = "http://rewardsservice:7050/rewardssearch"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_customers(self):
        response = requests.get(self.all_customers_url)
        return response.json()

    def get_single_customer(self):
        response = requests.get(self.single_customer_url)
        return response.json()
