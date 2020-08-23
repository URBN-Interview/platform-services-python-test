import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.orders_url = "http://rewardsservice:7050/order"
        self.all_users_url = "http://rewardsservice:7050/all-customer-rewards"
        self.single_user_url = "http://rewardsservice:7050/customer-rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_users(self):
        response = requests.get(self.all_users_url)
        return response.json()

    def get_user_reward(self, email_address):
        user_data = {"email_address": email_address}
        response = requests.get(self.single_user_url, params=user_data)
        return response.json()

    def add_order(self, email_address, order_total):
        order_data = {
            "email address": email_address,
            "order total": order_total
        }
        requests.post(self.orders_url, data=order_data)
