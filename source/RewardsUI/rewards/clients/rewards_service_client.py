import requests


class RewardsServiceClient:
    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.user_rewards_url = "http://rewardsservice:7050/rewards/users"
        self.rewards_order_url = "http://rewardsservice:7050/rewards/order"

    def get_all_tiers(self):
        all_tiers_response = requests.get(self.rewards_url)
        return all_tiers_response.json()

    def get_all_users(self, user_email=""):
        user_response = requests.get(
            self.user_rewards_url, params={"customerEmail": user_email}
        )
        return user_response.json()

    def get_single_user(self, user_email=""):
        single_user_response = requests.get(
            self.user_rewards_url, params={"customerEmail": user_email}
        )
        return single_user_response.json()

    def create_order(self, user_email="", order_total=0):
        order_response = requests.post(
            self.rewards_order_url,
            data={"customerEmail": user_email, "orderTotal": order_total},
        )
        return order_response.json()
