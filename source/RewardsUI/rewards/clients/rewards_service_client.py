import requests

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()


class AddedOrders:

    def __init__(self):
        self.addInfo_url = "http://rewardsservice:7050/info"

    def add_info(self):
        response = requests.post(self.addInfo_url)
        return response.json()

class GetAllInfo:

    def __init__(self):
        self.getAllInfo_url = "http://rewardsservice:7050/getall"

    def get_all_info(self):
        response = requests.get(self.getAllInfo_url)
        return response.json()
