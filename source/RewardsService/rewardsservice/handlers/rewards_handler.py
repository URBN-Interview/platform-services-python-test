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

            points = int(float(order_total))

            tier = None
            if points < 100:
                reward_tier_name = "A"
                progress = points / 100
                next_tier = "B"
            else:
                reward = self.db.rewards.find({}, {"_id": 0})

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
                        "rewardTierName": reward_tier_name, "progress": progress,
                        "nextTier": next_tier}

            self.db.customer_rewards.insert(response)
            self.write(dumps(response))

        except Exception as e:
            self.write(e)
            self.write_error(status_code=500)


class CustomerRewardHandler(BaseHandler):
    @coroutine
    def get(self):
        email_address = self.get_argument("email_address")
        rewards = self.db.customer_rewards.find_one({"emailAddress": email_address})
        self.write(dumps(rewards))


class ListCustomerRewardHandler(BaseHandler):
    @coroutine
    def get(self):
        rewards = list(self.db.customer_rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
