import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_add_url = "http://rewardsservice:7050/customers"
        self.customer_url = "http://rewardsservice:7050/customer"
        self.all_customers_url = "http://rewardsservice:7050/allCustomers"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def add_customers(self, email, total):
        data = {"email": email, "total": total}
        requests.post(self.customers_add_url, data)

    def get_customer(self, email):
        data = {"email" : email}
        res = requests.get(self.customer_url, params = data)
        return res.json()

    def get_customers(self):
        res = requests.get(self.all_customers_url)
        return res.json()
