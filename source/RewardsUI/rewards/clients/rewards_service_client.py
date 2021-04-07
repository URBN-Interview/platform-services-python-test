import requests


class RewardsServiceClient:
    #API endpoints to connect to services 
    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"
        self.all_customers_url = "http://rewardsservice:7050/allcustomers"
        self.customer_order_url = "http://rewardsservice:7050/customers"
        self.customer_data_url = "http://rewardsservice:7050/customer"

    #Funtions to retreive data in JSN format
    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

    def get_all_customers_data(self):
        response = requests.get(self.all_customers_url)
        return response.json()

    def send_customer_data(self, email_id, cust_order):
        response = requests.get(self.customer_order_url, params={"email":email_id, "order":cust_order})
        return {"status":response.status_code}

    def get_customer_data(self, email_id):
        response = requests.get("{}/{}".format(self.customer_data_url, email_id))
        if response.text == "Email ID not in the database":
            return {"status": "Email ID not in the database"}
        else:
            return response.json()
