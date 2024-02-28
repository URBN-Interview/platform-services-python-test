from collections import OrderedDict

from pymongo import MongoClient


class ComputationUtils:
    @classmethod
    def compute_rewards(cls):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        return list(db.rewards.find({}, {"_id": 0}))

    @classmethod
    def compute_rewards_for_users(cls, users_data):
        """

        :param users_data:  [{"email_address": "abc@xyz.com", "order_total": 100.8}]
        :return: [{

        }]

        [
      { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
      { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
      { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
      { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
      { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
      { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
      { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
      { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
      { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
      { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
  ]

  email_address	reward_points	reward_tier	reward_tier_name	next_reward_tier	next_reward_tier_name	next_reward_tier_progress
        """
        data = OrderedDict()
        records = cls.compute_rewards()
        data[0] = {"current": {}, "next": records[0]}
        for i in range(len(records)):
            data[records[i]["points"] // 100] = {"current": records[i], "next": records[i + 1] if i + 1 < len(records) else {}}

        output = []
        for user in users_data:
            email_address = user.get("email_address")
            order_total = user.get("order_total")
            points = min(order_total, 1001) // 100
            result = data.get(points)
            current = result.get("current")
            next = result.get("next")
            output.append({
                "email_address": email_address,
                "reward_points": order_total,
                "reward_tier": current.get("tier", ""),
                "reward_tier_name": current.get("rewardName", ""),
                "next_reward_tier": next.get("tier", ""),
                "next_reward_tier_name": next.get("rewardName", ""),
                "next_reward_tier_progress": "{} %".format(round((order_total * 100) / ((points + 1) * 100), 2)) if points < 10 else ""
            })

        return output

    @classmethod
    def compute_user_details_for_email_address(cls, email_address):
        """

        :param email_address: "email_address": "abc@xyz.com"
        :return:
        """

        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        if email_address:
            users = list(db.users.find({"email_address": email_address}, {"email_address": 1, "order_total": 1, "_id": 0}))
        else:
            users = list(db.users.find({}, {"email_address": 1, "order_total": 1, "_id": 0}))

        return cls.compute_rewards_for_users(users)

    @classmethod
    def add_order(cls, email_address, order_total):
        """

        :param email_address:
        :param order_total:
        :return: None
        """
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]

        user = db.users.find_one({"email_address": email_address}, {"_id": 0}) or {}
        old_order_total = user.get("order_total", 0)

        try:
            order_total = int(order_total)
        except ValueError:
            return False, "order_total should be integer"

        order_total += int(old_order_total)
        if email_address and order_total and not user:
            db.users.insert_one({"email_address": email_address, "order_total": order_total})

        elif email_address and user and order_total:
            db.users.update_one({"email_address": email_address}, {"$set": {"order_total": order_total}})

        elif not email_address or not order_total:
            return False, "Both Email address and order total should be present"

        return True, "Updated Successfully"


