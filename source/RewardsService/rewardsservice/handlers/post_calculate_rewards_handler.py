import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine

from rewardsservice.utils import email_is_valid, total_is_valid


class CalculateRewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        email = self.get_body_argument('email')
        existing_customer = db.customerdata.find_one({'email': email})
        rewards = list(db.rewards.find({}, {"_id": 0}))
        order_total = self.get_body_argument('order_total')

        if total_is_valid(order_total):
            points = int(float(order_total))
        else:
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Order total is not a valid number</body></html>")

        if email_is_valid(email):
            if existing_customer is not None:
                updated_points = existing_customer["rewardPoints"] + points
                tier = get_tier(updated_points, rewards)
                db.customerdata.update_one({'email': email}, {"$set": {"rewardPoints": updated_points,
                                                                       "rewardTierName": tier["reward_name"],
                                                                       "rewardTier": tier["tier"],
                                                                       "nextTier": tier["next_tier"],
                                                                       "nextTierName": tier["next_tier_name"]}})
            else:
                tier = get_tier(points, rewards)
                db.customerdata.insert_one({"email": email,
                                            "rewardPoints": points,
                                            "rewardTierName": tier["reward_name"],
                                            "rewardTier": tier["tier"],
                                            "nextTier": tier["next_tier"],
                                            "nextTierName": tier["next_tier_name"]})
        else:
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Invalid email</body></html>")


def get_tier(points, rewards):
    """Returns tier info

    :param points: integer
    :param rewards: list of reward objects
    :return: dict of tier data
    """
    tier_dict = {}
    length = len(rewards) - 1
    rewards = sorted(rewards, key=lambda x: x['points'])

    for i in range(0, length):
        j = i + 1
        if rewards[i]['points'] <= points < rewards[j]['points']:
            tier_dict = {
                "tier": rewards[i]['tier'],
                "reward_name": rewards[i]['rewardName'],
                "next_tier": rewards[j]['tier'],
                "next_tier_name": rewards[j]['rewardName']}

        elif points < rewards[0]['points']:
            tier_dict = {
                "tier": "",
                "reward_name": "",
                "next_tier": rewards[0]['tier'],
                "next_tier_name": rewards[0]['rewardName']}

        elif points >= rewards[length]['points']:
            tier_dict = {
                "tier": rewards[length]['tier'],
                "reward_name": rewards[length]['rewardName'],
                "next_tier": "",
                "next_tier_name": ""}

    return tier_dict
