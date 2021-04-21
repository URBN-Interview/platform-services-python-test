import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.AllCustomer_url = "http://rewardsservice:7050/customers"
        self.OneCustomer_url = "http://rewardsservice:7050/customer"


    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    def get_Single_Customer(self, email):
        response = requests.get(self.OneCustomer_url,{"email":email})
        return response.json()
    def get_Customers(self):
        response = requests.get(self.AllCustomer_url)
        return response.json()