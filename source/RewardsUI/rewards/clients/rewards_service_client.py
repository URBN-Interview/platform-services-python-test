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
        return

    def get_customer(self, email):
        data = {"email" : email}
        res = request.get(self.customer_url, params = data)
        return res.json()
