import requests
import tornado.escape
import json

def test_post_customer_order():
    data = json.dumps({"Email Address":"test@test.com", "Order Total":100.80})
    response = requests.post("http://localhost:7050/customerOrderData", data=data)
    response = str(response)
    assert response == "<Response [200]>"

