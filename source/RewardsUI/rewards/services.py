import requests
def get_all_user_rewards(url="http://127.0.0.1:7050/endpoint_three"):
    r = requests.get(url)
    return r.json()

