import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.order_url = "http://rewardsservice:7050/order"
        self.customer_url = "http://rewardsservice:7050/customer/"
        self.customers_url = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    #post orders function
    def post_order(self, orderData):
        response = requests.post(self.order_url, data = orderData)
        return None
    #get customer based off search 
    def get_customer(self, email):
        response = requests.get(self.customer_url, {"email": email})
        return response.json()
    