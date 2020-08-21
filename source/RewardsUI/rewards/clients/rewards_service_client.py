import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.all_customers_url = "http://rewardsservice:7050/allcustomers"
        self.single_customer_url = "http://rewardsservice:7050/customer"
        self.add_order_url =  "http://rewardsservice:7050/order"


    #gets all the rewards in the system
    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    #gets a single customer reward
    def get_customer(self, emailAddress):
        response = requests.get(self.single_customer_url, {"emailAddress": emailAddress})
        return response.json()

    #gets all the customer rewards in the system
    def get_all_customers(self):
        response = requests.get(self.all_customers_url)
        return response.json()

    #add an order using by inputting an email address and an order total
    def add_order(self, emailAddress, orderTotal):
        response = requests.post(url=self.add_order_url, data={"emailAddress": emailAddress, "orderTotal": orderTotal})
        # print(response)
        # return response.json()


