import requests
# import json

class Endpoint1Client:

    def __init__(self):
        self.endpoint1_url = r"http://127.0.0.1:7050/endpoint1"
        self.params = {}
        # replaced 'rewardsservice' with localhost to get django project up

    def add_order(self, email, order_total, *args, **kwargs):
        params = {
            'email': email, 
            'order_total': order_total
        }
        # endpoint1_url = "http://127.0.0.1:7050/endpoint1/" + f"{email}" + "/" + f"{order_total}"
        r = requests.post(self.endpoint1_url, data=params)
        response = r.text
        return response