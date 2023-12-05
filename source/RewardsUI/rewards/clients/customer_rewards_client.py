import requests


class CustomerRewardsClient:

    def __init__(self):
        pass

    # def get_customer(self, email):
    #     response = requests.get(f"http://rewardsservice:7050/customers/{email}")
    #     return response.json()

    def get_customer_list(self):
        response = requests.get("http://rewardsservice:7050/customers")
        return response.json()
