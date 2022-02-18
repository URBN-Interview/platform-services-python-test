import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_order_url = "http://rewardsservice:7050/orders"
        self.all_customers = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    
    # customer_order
    # handler for submitting customer order info to API
    def customer_order(self, order):
        response = requests.post(self.customer_order_url, data=order)
        return response.json()
    
    # all customers
    # handlers to grab all customer data from API
    def all_customer(self):
        response = requests.get(self.all_customer)
        return response.json()
