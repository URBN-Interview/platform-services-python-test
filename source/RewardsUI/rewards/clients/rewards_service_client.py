import requests
import json

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.all_customer_rewards_url = "http://rewardsservice:7050/customer_rewards"
        self.customer_order_rewards_url = "http://rewardsservice:7050/customer_order_rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)        
        return response.json()

    def get_all_customer_rewards(self):
        response = requests.get(self.all_customer_rewards_url)
        return response.json()

    def post_customer_order(self, customer_email_address, customer_order):
        response = requests.post(self.customer_order_rewards_url, data=json.dumps(
            ({"email": customer_email_address, "order_total": customer_order}))
            )
        print("post_customer_order: ", json.loads(response.text))
        return response

    def post_customer_reward(self, customer_email_address):
        response = requests.post(self.all_customer_rewards_url, data=json.dumps(
            ({"email": customer_email_address})))
        print("post_customer_order: ", json.loads(response.text))
        return response    