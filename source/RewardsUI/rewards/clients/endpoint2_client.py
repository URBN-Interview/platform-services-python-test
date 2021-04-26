import requests
import json

class Endpoint2Client:

    def __init__(self):
        self.endpoint2_url = "http://127.0.0.1:7050/endpoint2"
        self.params = {}

    def search_user(self, email):
        params = {
            'email': email
        }
        return requests.get("http://127.0.0.1:7050/endpoint2", params=params)