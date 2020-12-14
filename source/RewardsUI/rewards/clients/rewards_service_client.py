from urllib import parse

import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_data_url = "http://rewardsservice:7050/customer_data"
        self.user_rewards_url = "http://rewardsservice:7050/customer_rewards"
        self.calculate_rewards_url = "http://rewardsservice:7050/calculate_rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_customer_data(self):
        response = requests.get(self.customer_data_url)
        return response.json()

    def get_user_rewards(self, email):
        response = requests.get(self.user_rewards_url, data=({'email': email}))
        return response.json()

    def post_calculate_rewards(self, email, order_total):
        requests.post(self.calculate_rewards_url, data={'email': email,
                                                        'order_total': order_total})
