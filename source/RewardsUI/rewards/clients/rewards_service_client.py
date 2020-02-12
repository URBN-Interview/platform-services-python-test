import requests

import logging
logger = logging.getLogger(__name__)

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_order_url = "http://rewardsservice:7050/customerorder"
        self.get_customer_reward_url = "http://rewardsservice:7050/getcustomerreward"
        self.all_customers_reward_url = "http://rewardsservice:7050/allcustomersreward"



    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def customer_order(self,email_address,order_total):
        response = requests.post(url=self.customer_order_url, data={"email": email_address, "total": order_total})
        return response.json()

    def get_customer_reward(self,email_address):
        response = requests.get(self.get_customer_reward_url,{"email":email_address})
        return response.json()

    def get_all_customers_reward(self):
        response = requests.get(self.all_customers_reward_url)
        return response.json()