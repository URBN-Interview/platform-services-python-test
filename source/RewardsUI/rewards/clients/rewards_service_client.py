import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.insert_url = "http://rewardsservice:7050/insert"
        self.find_url = "http://rewardsservice:7050/find"
        self.all_url = "http://rewardsservice:7050/all"

    #Return the response from endpoint http://localhost:7050/rewards
    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    #Return the response from endpoint http://localhost:7050/insert?email=example@email.com&total=100
    def insert_order(self, email, total):
        urlBuilder = self.insert_url + "?email=" + str(email) + "&total=" + str(total)
        response = requests.get(urlBuilder)
        return response.json()

    #Return the response from endpoint http://localhost:7050/find?email=example@email.com
    def find_customer(self, user):
        response = requests.get(self.find_url + "?email=" + str(user))
        return response.json()

    #Return the response from endpoint http://localhost:7050/all
    def all_customers(self):
        response = requests.get(self.all_url)
        return response.json()