import requests


class CustomerServiceClient:

    def __init__(self):
        self.customers_url = "http://rewardsservice:7050/customers"
        self.customer_url = "http://rewardsservice:7050/customer"
        self.update_customer_url = "http://rewardsservice:7050/updateCustomer"

    def getCustomer(self, email):
        response = requests.get(self.customer_url, param={"email": email})
        return response.json()

    def getAllCustomers(self):
        response = requests.get(self.customers_url)
        return response.json()

    def postCustomer(self, email, total):
        response = requests.post(self.update_customer_url, params={
                                 "email": email, "total": total})
        return response.json()
