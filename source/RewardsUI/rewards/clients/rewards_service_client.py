import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.customer_url = "http://rewardsservice:7050/customer"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def get_customer(self, email_address):
        url = self.customer_url + '?email_address={}'.format(email_address)
        response = requests.get(url)
        return response.json()