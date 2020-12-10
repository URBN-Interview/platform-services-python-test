import requests


class RewardsServiceClient:

    def __init__(self):
        self.rewards_url = "http://rewardsservice:7050/rewards"

    def get_rewards(self):
        response = requests.get(self.rewards_url)
        return response.json()

class RewardMembersClient:

    def __init__(self):
        self.members_url = "http://rewardsservice:7050/rewardMembers"

    def get_members(self):
        response = requests.get(self.members_url)
        return response.json()

class OrderClient:

    def __init__(self):
        self.members_url = "http://rewardsservice:7050/postData"

    def post_order(self, json):
        r = requests.post(self.members_url, json=json)

class FindMemberClient:

    def __init__(self):
        self.members_url = "http://rewardsservice:7050/getRewards"

    def get_member(self, json):
        response = requests.post(self.members_url, json=json)

        print(response.json(), flush=True)

        if response.status_code == 200:
            return response.json()
