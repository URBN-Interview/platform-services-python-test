import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_url = "http://rewardsservice:7050/customer"	
        self.customers_url = "http://rewardsservice:7050/customers"	
        self.order_url = "http://rewardsservice:7050/order"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

# get specific customer	
    def get_customer(self, email):	
        response = requests.get(self.customer_url, {"email": email})	
        return response.json()	
# get all customers	
    def get_customers(self):	
        response = requests.get(self.customers_url)	
        return response.json()	
# get eamil and order	
    def get_order(self, email, orderTotal):	
        response = requests.post(self.order_url, data={"email": email, "orderTotal": orderTotal}) 	
        return response.json()
