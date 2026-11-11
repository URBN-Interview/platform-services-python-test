# HTTP client for the RewardsService API. Keeps all calls to the backend in one
# place so views never build URLs or parse responses themselves.

import requests


class RewardsServiceClient:
    """Thin wrapper around `requests` for talking to RewardsService.

    Uses the Docker hostname `rewardsservice` (reachable because the UI
    container joins the rewardsservice_default network).
    get_rewards(): GET /rewards and return the parsed JSON list of tiers.
    """


    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()
