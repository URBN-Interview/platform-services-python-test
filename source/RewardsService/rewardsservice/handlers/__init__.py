import re
import tornado.web
from pymongo import MongoClient


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

    def status_code_and_reason(self, status_code, message, code):
        self.set_status(status_code)
        self.finish({"message": message, "code": code})

    def check_order_total_type(self, order_total):
        try:
            int(float(order_total))
        except ValueError:
            self.status_code_and_reason(400, "Order total must be number(s)", "VALIDATION_ERROR")

    def check_email_address(self, email):
        email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(email_regex, email):
            return
        else:
            self.status_code_and_reason(400, "Email Address has to be in email format", "VALIDATION_ERROR")
