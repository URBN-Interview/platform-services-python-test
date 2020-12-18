import requests
import json


class CustomersClient:

    def __init__(self):
        self.baseUrl = "http://rewardsservice:7050/"

    def get_customers(self):
        response = requests.get(self.baseUrl + "customers")
        try:
            return response.json()
        except:
            return []

    def get_customer(self, email):
        response = requests.get(
            self.baseUrl + "customer", params={"email": email.strip()})
        try:
            return response.json()
        except:
            return {}

    def post_order(self, email, orderTotal):
        response = requests.post(
            self.baseUrl + "order", data=json.dumps({"email": email.strip(), "orderTotal": float(orderTotal)}))
        try:

            return response.json()
        except:
            return
