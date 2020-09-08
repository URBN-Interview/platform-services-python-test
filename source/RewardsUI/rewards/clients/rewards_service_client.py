import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/allCustomers"
        self.customer_url = "http://rewardsservice:7050/customer/"
        self.order_url = "http://rewardsservice:7050/order/"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def get_customer(self, email):

        payload = {'email': email}

        response = requests.get(self.customer_url, params=payload)
        return response.json()

    def post_order(self, order):

        response = requests.post(self.order_url, params=order)
        return response.json()



    