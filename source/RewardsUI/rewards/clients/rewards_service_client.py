import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.add_orders_url = "http://rewardsservice:7050/rewardpoint"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    
    def add_orders(self, email, order_total):
        response = requests.post(self.add_orders_url, data={"email": email , "order_total": order_total})
        return response.json()

