"""
Client for the Customer endpoint
"""
import json
import requests

class CustomerServiceClient:

    def __init__(self):
        self.customer_url = "http://rewardsservice:7050/customers"

    def get_customers(self):
        try:
            response = requests.get(self.customer_url)
            return response.json()
        except Exception as err:
            raise err
    
    def get_customer(self, email):
        try:
            response = requests.post(
                self.customer_url,
                data=json.dumps({"email": email})
            )
            
            return response.json()
        except Exception as err:
            raise err