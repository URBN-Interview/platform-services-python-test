import json
import requests


class RewardsServiceClient:

    def __init__(self):
        self.base_url = "http://rewardsservice:7050"
        self.rewards_url = f"{self.base_url}/rewards"
        self.customer_data_url = f"{self.base_url}/customer/rewards/"
        self.customers = f"{self.base_url}/customer/rewards/"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        response = response.json()
        if response.get("status") == "SUCCESS":
            return response.get("results")
        return response.json()

    def get_customer_data(self, email):
        response = requests.get(f"{self.customer_data_url}{email}")
        response = response.json()
        if response.get("status") == "SUCCESS":
            return response.get("results", [])
        return []

    def get_customers(self):
        response = requests.get(self.customer_data_url)
        response = response.json()
        if response.get("status") == "SUCCESS":
            return response.get("results", [])
        return []

    def process_order(self, email, order_total):
        payload = json.dumps({"email": email, "order_total": order_total})
        response = requests.post(self.customer_data_url, data=payload)
        response = response.json()
        if response.get("status") == "SUCCESS":
            return True
        else:
            return response.get("errors", {})
