import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.all_customers_url = "http://rewardsservice:7050/allcustomers"
        self.add_order_url = "http://rewardsservice:7050/customer"


    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customer(self, email_address):
        response = requests.get(self.add_order_url, {"emailAddress": email_address})
        return response.json()

    def get_all_customers(self):
        response = requests.get(self.all_customers_url)
        return response.json()

    def add_order(self, email_address, order_total):
        response = requests.post(url=self.rewards, data={"emailAddress": email_address, "orderTotal": order_total})

