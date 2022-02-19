"""
Client for the Customer endpoint
"""
import json
import requests

class CustomerServiceClient:

    def __init__(self):
        self.customer_url = "http://rewardsservice:7050/customers"

    def get_customers(self):
        response = requests.get(self.customer_url)
        return response.json()
    
    def get_customer(self, email):
        response = requests.post(
            self.customer_url,
            data=json.dumps({"email": email})
        )
        
        return response.json()