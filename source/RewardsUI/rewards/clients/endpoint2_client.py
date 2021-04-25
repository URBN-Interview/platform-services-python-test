import requests

class Endpoint2Client:

    def __init__(self):
        self.endpoint2_url = "http://127.0.0.1:7050/endpoint2"
        self.params = {}
        # replaced 'rewardsservice' with localhost to get django project up

    def search_user(self, email, *args, **kwargs):
        params = {
            'email': email
        }
        requests.post(self.endpoint2_url, data=params)
        # response = r.text
        # return response