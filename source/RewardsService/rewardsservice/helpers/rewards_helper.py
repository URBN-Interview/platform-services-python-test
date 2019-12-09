from pymongo import MongoClient


def _calculate_rewards_status(db, points):
    # rewards in descending order for easier search implementation
    rewards_desc = list(db.rewards.find({}, {"_id": 0}).sort("points", -1))
    reward, reward_idx = next((reward, idx)
                              for idx, reward in enumerate(rewards_desc)
                              if reward["points"] < points)

    next_reward_idx = reward_idx - 1

    reward_status = {}
    reward_status["points"] = points
    reward_status["tier"] = reward["tier"]
    reward_status["rewardName"] = reward["rewardName"]

    if next_reward_idx >= 0:
        next_reward = rewards_desc[next_reward_idx]
        reward_status["nextTier"] = next_reward["tier"]
        reward_status["nextRewardName"] = next_reward["rewardName"]
        next_reward_points = next_reward["points"] - points
        next_reward_progress = \
            next_reward_points / (next_reward["points"] - reward["points"])
        reward_status["nextRewardProgress"] = next_reward_progress

    return reward_status


def update_rewards(email):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]

    customer_points_total_query = db.orders.aggregate([{
        "$match": {
            "email": email
        }
    }, {
        "$group": {
            "_id": None,
            "total": {
                "$sum": {
                    "$floor": "$amount"
                }
            }
        }
    }])

    customer_points_total = list(customer_points_total_query)[0]["total"]
    reward_status = _calculate_rewards_status(db, customer_points_total)

    reward_status.update(({"email": email}))
    db.customer_rewards.replace_one({"email": email}, reward_status, True)
