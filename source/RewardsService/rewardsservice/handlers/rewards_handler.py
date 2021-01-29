import json

from bson.json_util import dumps

from tornado.gen import coroutine
from tornado.web import MissingArgumentError

from handlers import BaseHandler


class RewardsHandler(BaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    @coroutine
    def post(self):
        try:
            try:
                email_address = self.get_argument("email_address")
                order_total = self.get_argument("order_total")
            except MissingArgumentError:
                self.status_code_and_reason(400, "Please provide email address and order total", "VALIDATION_ERROR")

            self.check_order_total_type(order_total)
            self.check_email_address(email_address)

            check_existing = self.db.customer_rewards.find_one({"emailAddress": email_address})
            points = int(float(order_total))

            if not check_existing:
                if points < 100:
                    progress = points / 100
                    next_tier = "A"
                    tier = None
                    reward_tier_name = None

                else:
                    reward = self.db.rewards.find({}, {"_id": 0})
                    calculate_points = self.calculate_points(email_address, reward, points)
                    email_address = calculate_points.get("emailAddress")
                    points = calculate_points.get("points")
                    tier = calculate_points.get("tier")
                    reward_tier_name = calculate_points.get("rewardTierName")
                    progress = calculate_points.get("progress")
                    next_tier = calculate_points.get("nextTier")

                response = {"emailAddress": email_address, "points": points, "tier": tier,
                            "rewardTierName": reward_tier_name, "progress": progress,
                            "nextTier": next_tier}

                self.db.customer_rewards.insert(response)
                self.write(dumps(response))

            else:
                updated_points = check_existing.get("points") + points

                if updated_points < 100:
                    progress = updated_points / 100
                    next_tier = "A"
                    tier = None
                    reward_tier_name = None

                    response = {"emailAddress": email_address, "points": updated_points, "tier": tier,
                            "rewardTierName": reward_tier_name, "progress": progress,
                            "nextTier": next_tier}

                else:
                    reward = self.db.rewards.find({}, {"_id": 0})
                    response = self.calculate_points(email_address, reward, updated_points)

                self.db.customer_rewards.update_one({"emailAddress": email_address}, {"$set": response})
                self.write(dumps(response).encode("utf-8"))

        except Exception as e:
            self.write(e)
            self.write_error(status_code=500)


class CustomerRewardHandler(BaseHandler):
    @coroutine
    def get(self):
        try:
            email_address = self.get_argument("email_address")
        except MissingArgumentError:
            self.status_code_and_reason(400, "Please provide email address", "VALIDATION_ERROR")

        self.check_email_address(email_address)
        rewards = self.db.customer_rewards.find_one({"emailAddress": email_address})
        self.write(dumps(rewards).encode("utf-8"))


class ListCustomerRewardHandler(BaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.customer_rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
