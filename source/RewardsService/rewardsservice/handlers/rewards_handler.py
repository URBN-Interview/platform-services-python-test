import json
from bson.json_util import dumps

from tornado.gen import coroutine

from handlers import validate_email, BaseHandler, validate_order_total


class RewardsHandler(BaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

    @coroutine
    def post(self):
        try:
            email_address = self.get_argument("email_address")
            order_total = self.get_argument("order_total")

            if not email_address or not order_total:
                self.write_error(status_code=500)

            if not validate_email(email_address):
                self.write_error(status_code=500)

            if not validate_order_total(order_total):
                self.write_error(status_code=500)

            check_existing = self.db.customer_rewards.find_one({"emailAddress": email_address})
            points = int(float(order_total))

            if not check_existing:
                if points < 100:
                    reward_tier_name = "A"
                    progress = points / 100
                    next_tier = "B"
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
        email_address = self.get_argument("email_address")
        rewards = self.db.customer_rewards.find_one({"emailAddress": email_address})
        self.write(dumps(rewards).encode("utf-8"))


class ListCustomerRewardHandler(BaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.customer_rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
