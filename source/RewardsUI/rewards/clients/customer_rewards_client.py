import requests

# this is being added to the get handlers on the view so that it will load when the template mounts


class CustomerRewardsClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/admin"
        self.customers_url = "http://rewardsservice:7050/customers"

    def get_all(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_one(self, data):
        response = requests.get(self.customers_url, json=data)
        return response.json()

    def update_record(self, data):
        requests.post(self.customers_url, json=data)
