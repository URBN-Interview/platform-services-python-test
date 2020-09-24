import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.all_customers_url = "http://rewardsservice:7050/allcustomers"
        self.order_url = "http://rewardsservice:7050/order"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
    def get_customers(self,email):
        response = requests.get(self.customers_url,{"email":email})
        return response.json()
    def get_all_customers(self):
        response = requests.get(self.all_customers_url)
        return response.json()
    def get_order(self, email, orderTotal):
        response = requests.post(self.order_url, data={"email": email, "orderTotal": orderTotal})
        return response.json()
