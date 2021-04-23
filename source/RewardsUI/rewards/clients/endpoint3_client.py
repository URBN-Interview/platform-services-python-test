import requests

class Endpoint3Client:

    def __init__(self):
        self.users_url = "http://127.0.0.1:7050/endpoint3"
        # replaced 'rewardsservice' with localhost to get django project up

    def get_all_users(self):
        response = requests.get(self.users_url)
        return response.json()
