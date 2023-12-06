import requests
import json

url = "http://localhost:7050/customers"

def test_customer_list_connection():
    response = requests.get(url)
    assert response.status_code == 200

def test_get_single_customer_by_email():
    list_response = requests.get(url)
    single_email = list_response.json()[0]["email"]
    response = requests.get(url + "/" + single_email)
    customer = response.json()

    assert customer["points"] is not None
    assert customer["email"] is not None
    assert customer["name"] is not None
    assert response.status_code == 200

def test_update_points():
    get_response = requests.get(url)
    customer = get_response.json()[0]
    points = customer["points"]
    email = customer["email"]
    order_amount = 100.99
    body = json.dumps({"order": order_amount})
    update_response = requests.put(url + "/" + email, data=body)

    assert update_response.status_code == 200
    get_single_response = requests.get(url + "/" + email)
    assert get_single_response.status_code == 200
    new_points = get_single_response.json()["points"]
    assert new_points - points == (order_amount // 1)
