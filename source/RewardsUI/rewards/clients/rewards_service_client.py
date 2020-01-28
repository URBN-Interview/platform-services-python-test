import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.send_order_data_url = "http://rewardsservice:7050/order_data?email_address="
        self.search_rewards_data_url = "http://rewardsservice:7050/find_rewards_data?email_address="
        self.all_rewards_data = "http://rewardsservice:7050/all_rewards_data"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def send_order_data(self, email, total):
        response = requests.get(
            self.send_order_data_url + email+"&&"+"order_total="+total)

    def search_rewards_data(self, email):
        response = requests.get(
            "http://rewardsservice:7050/find_rewards_data?email_address="+email)
        return response.json()

    def get_all_rewards(self):
        response = requests.get(self.all_rewards_data)
        return response.json()
