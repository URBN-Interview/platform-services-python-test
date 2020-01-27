import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.send_order_data_url = "http://rewardsservice:7050/order_data?email_address="

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def send_order_data(self, email, total):
        response = requests.get(
            self.send_order_data_url + email+"&&"+"order_total="+total)
