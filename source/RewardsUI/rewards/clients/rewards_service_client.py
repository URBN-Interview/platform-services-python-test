import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.orders_url = "http://rewardsservice:7050/orders"
        self.customer_url = "http://rewardsservice:7050/customer"
        self.customers_url = "http://rewardsservice:7050/customers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_customers(self, email, total):
        data = {"email": email, "total": total}
        requests.post(self.orders_url, data)

    def get_customer(self, email):
        data = {"email" : email}
        res = requests.get(self.customer_url, params = data)
        return res.json()

    def get_customers(self):
        res = requests.get(self.customers_url)
        return res.json()
