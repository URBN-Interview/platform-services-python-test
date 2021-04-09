import requests


class AllUserInfoServiceClient:

    def __init__(self):
        self.all_user_info_url = "http://rewardsservice:7050/retrieve_all_user_info"

    def get_all_user_info(self):
        response = requests.get(self.all_user_info_url)
        return response.json()
