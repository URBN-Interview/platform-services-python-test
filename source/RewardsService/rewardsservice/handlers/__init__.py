import re
import tornado.web
from pymongo import MongoClient

email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def validate_email(email):
    if re.search(email_regex, email):
        return True
    else:
        return False


def validate_order_total(order_total):
    if re.match(r'^-?\d+(?:\.\d+)?$', order_total) is not None:
        return True
    else:
        return False


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        client = MongoClient("mongodb", 27017)
        self.db = client["Rewards"]

    def calculate_points(self, email_address, reward, points):
        tier = None

        for t in reward:
            previous_tier = t.get("points", 0)

            if previous_tier > points:
                next_tier = t.get("tier")
                progress = points / previous_tier
                break

            elif points > previous_tier and tier is not None:
                next_tier = None
                progress = 0

            tier = t.get("tier", "")
            reward_tier_name = t.get("rewardName", "")

        response = {"emailAddress": email_address, "points": points, "tier": tier,
                    "rewardTierName": reward_tier_name, "progress": progress, "nextTier": next_tier}
        return response
