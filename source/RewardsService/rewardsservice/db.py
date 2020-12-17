import json
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.collection import ReturnDocument
from bson import json_util

class Database():
    def __init__(self):
        self.client = MongoClient("mongodb", 27017)

    def upsert_customer(self, email_address, order_total):
        db = self.client["Customers"]

        customer_exists = db.customers.count_documents({'email_address': email_address}) > 0
        if not customer_exists:
            record = self.new_customer_record(email_address, order_total)
            db.customers.insert(record)

        customer = list(db.customers.find({'email_address': email_address}))[0]
        return json.loads(json_util.dumps(customer))

    def new_customer_record(self, email_address, order_total):
        return {
            "email_address": email_address,
            **self.new_reward_data_for_order_total(order_total)
        }

    def new_reward_data_for_order_total(self, order_total):
        points = int(order_total) # rounds down
        current_tier = self.get_current_tier_by_points(points)
        next_tier = self.get_next_tier_by_points(points)

        return {
            "reward_points": current_tier.get("points", ""),
            "reward_tier": current_tier.get("tier", ""),
            "reward_tier_name": current_tier.get("rewardName", ""),
            "next_reward_tier": next_tier.get("points", ""),
            "next_reward_tier_name": next_tier.get("tier", ""),
            "next_reward_tier_progress": next_tier.get("rewardName", "")
        }

    def get_current_tier_by_points(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$lte": points}}).sort('points', DESCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))

    def get_next_tier_by_points(self, points):
        db = self.client["Rewards"]
        tier_list = list(db.rewards.find({"points": {"$gt": points}}).sort('points', ASCENDING))
        if len(tier_list) == 0:
            return {}
        return json.loads(json_util.dumps(tier_list[0]))