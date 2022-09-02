import requests
import tornado.escape
import json


def test_get_single_customer_order():
    data = json.dumps({"Email Address":"test@test.com"})
    response = requests.get("http://localhost:7050/singleCustomerRewardsData", data=data)
    response = str(response)
    assert response == "<Response [200]>"

def test_get_all_customer_orders():
    response = requests.get("http://localhost:7050/customerRewardsData")
    response = str(response)
    assert response == "<Response [200]>"