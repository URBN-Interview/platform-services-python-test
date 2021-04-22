import requests

class Endpoint1Client:

    def __init__(self):
        self.endpoint1_url = "http://127.0.0.1:7050/endpoint1"
        # replaced 'rewardsservice' with localhost to get django project up

    def add_order(self):
        response = requests.get(self.endpoint1_url)
        return response.json()