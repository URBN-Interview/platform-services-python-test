import requests
import json

class CustomerRewardsClient:

    def __init__(self):
        self.customer_url = "http://rewardsservice:7050/customers"

    def get_customer(self, email):
        response = requests.get(self.customer_url + "/" + email)
        return response.json()

    def get_customer_list(self):
        response = requests.get(self.customer_url)
        return response.json()

    def update_customer_rewards(self, email, order):
        request_url = "http://rewardsservice:7050/customers/" + email
        body = json.dumps({"order": float(order)})
        response = requests.put(request_url, data=body)
        return response.json()
