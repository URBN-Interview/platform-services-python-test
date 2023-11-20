import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.submit_order_url = "http://rewardsservice:7050/order/rewards"
        self.customer_rewards_url = "http://rewardsservice:7050/user/rewards"
        self.all_customers_rewards_url = "http://rewardsservice:7050/allcustomers/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def submit_order(self, email, order_total):
        params = {"email": email, "order_total": order_total}
        response = requests.post(self.submit_order_url, params=params)
        # testing purpose
        #print("inside submit", response.json())
        #print(response)  
        return response

    def get_customer_rewards(self, email):
        params = {"email": email}
        response = requests.get(self.customer_rewards_url, params=params)
        return response.json()

    def get_all_customers_rewards(self):
        response = requests.get(self.all_customers_rewards_url)
        return response.json()

