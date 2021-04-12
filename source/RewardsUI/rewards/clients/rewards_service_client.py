import requests
import urllib.parse as urlparse
from urllib.parse import parse_qs

class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.customer_rewards_url = "http://rewardsservice:7050/customerrewards"
    
    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_customers(self):
        response = requests.get(self.customer_rewards_url, params=None)
        return response.json()

    def get_customer_rewards(self):
        parsed = urlparse.urlparse(self.customer_rewards_url)
        email = parse_qs(parsed.query, keep_blank_values=True)['email']
        ordertotal = parse_qs(parsed.query, keep_blank_values=True)['ordertotal']
        params = {'email':email, 'ordertotal':ordertotal}
        
        response = requests.get(self.customer_rewards_url, params=params)
        return response.json()