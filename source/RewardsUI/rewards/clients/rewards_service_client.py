import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.single_customers_url = "http://rewardsservice:7050/customers/*"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def get_single_customer(self, email):
        response = requests.get(self.single_customers_url, data=({"email": email}))
        print("Get_single_ response: ", response)
        return response.json()