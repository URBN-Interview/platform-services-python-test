import requests
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator


class RewardsServiceClient:

    def __init__(self):
        self.base_url = "http://rewardsservice:7050"
        self.rewards_url = self.base_url + "/rewards"
        self.customer_rewards_url = self.base_url + "/me/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def post_rewards(self, email_address, amount):
        method_decorator(csrf_protect)
        response = requests.post(self.rewards_url,
                                 params={"email_address": email_address, "order_total": amount})
        return response.json()

    def get_customers(self, email_address):
        method_decorator(csrf_protect)
        response = requests.get(self.customer_rewards_url, params={"email_address": email_address})
        return response.json()
