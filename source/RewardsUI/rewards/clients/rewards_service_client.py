import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.all_customers_url = "http://rewardsservice:7050/customers/all"
        self.orders_url = "http://rewardsservice:7050/orders"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customer(self, email):
        response = requests.get(self.customers_url, {"Email Address": email})
        return response.json()
    
    def get_all_customers(self):
        response = requests.get(self.all_customers_url)
        return response.json()

    def get_orders(self):
        response = requests.get(self.orders_url)
        return response.json()
        
