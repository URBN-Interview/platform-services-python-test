import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customers_url = "http://rewardsservice:7050/customers"
        self.customer_url = "http://rewardsservice:7050/customerrewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_customers(self):
    	response = requests.get(self.customers_url)
    	return response.json()

    def get_customer(self, email_address):
    	response = requests.get(self.customer_url, {"emailAddress": email_address})
    	return response.json()

    def add_order_rewards(self, email_address, order_total):
    	response = requests.post(url=self.customer_url, data={"emailAddress": email_address, "orderTotal": order_total})
