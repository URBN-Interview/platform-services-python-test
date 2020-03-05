import requests


class RewardsServiceClient:

    def __init__(self, endpoint):
        self.url = "http://rewardsservice:7050/"
        self.endpoint = endpoint


    def request(self, context=None):
        if context is not None:
            response = requests.get(self.url + self.endpoint, context)
        else:
            response = requests.get(self.url + self.endpoint)

        body = response.json()
        if(type(body) != list and body.error):
            raise Exception(body.type)
        else:
            return body



class RewardsRequest(RewardsServiceClient):

    def __init__(self):
        self.endpoint = "rewards"
        super().__init__(self.endpoint)

class AllCustomersRequest(RewardsServiceClient):

    def __init__(self):
        self.endpoint = "customers"
        super().__init__(self.endpoint)

class CustomerRequest(RewardsServiceClient):

    def __init__(self):
        self.endpoint = "customer"
        super().__init__(self.endpoint)

class OrderRequest(RewardsServiceClient):

    def __init__(self):
        self.endpoint = "order"
        super().__init__(self.endpoint)
