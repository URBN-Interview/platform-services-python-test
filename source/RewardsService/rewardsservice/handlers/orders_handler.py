import json

from handlers.base_handler import BaseHandler
from services.rewards_calculator import calculate_rewards, points_earned_for_order


class OrdersHandler(BaseHandler):

    async def post(self):
        body = self.get_json_body()
        email = self.validate_email(body.get("email"))
        order_total = self.validate_order_total(body.get("orderTotal"))

        db = self.application.db
        tiers = await db.rewards.find({}, {"_id": 0}).to_list(length=None)

        existing = await db.customerRewards.find_one({"email": email}, {"_id": 0})
        previous_points = existing["rewardPoints"] if existing else 0

        earned_points = points_earned_for_order(order_total)
        total_points = previous_points + earned_points

        reward_data = calculate_rewards(total_points, tiers)
        reward_data["email"] = email

        await db.customerRewards.update_one(
            {"email": email}, {"$set": reward_data}, upsert=True
        )

        self.set_status(201)
        self.write(json.dumps(reward_data))
