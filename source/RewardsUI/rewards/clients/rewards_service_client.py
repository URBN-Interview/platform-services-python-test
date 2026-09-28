import requests


class RewardsServiceError(Exception):
    pass


class RewardsServiceClient:

    def __init__(self):
        self.base_url = "http://rewardsservice:7050"

    def request(self, method, path, **kwargs):
        try:
            response = requests.request(method, self.base_url + path, timeout=5, **kwargs)
        except requests.RequestException:
            raise RewardsServiceError("The rewards service is not reachable.")
        if response.status_code >= 400:
            raise RewardsServiceError(response.json()["error"]["message"])
        return response.json()

    def get_rewards(self):
        return self.request("GET", "/rewards")

    def get_customers(self):
        return self.request("GET", "/customers")

    def get_customer(self, email):
        return self.request("GET", "/customer/" + email)

    def add_order(self, email, order_total):
        return self.request("POST", "/customer", json={"email_address": email, "order_total": order_total})
