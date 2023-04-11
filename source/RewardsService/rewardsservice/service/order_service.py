import pymongo

from source.RewardsService.rewardsservice.dao.mongo_client import MongoDao


class OrderService:
    """"
    Created OrderService to differentiate end point controller to use code in service layer
    Got some issue while importing package.
    """
    def __init__(self):
        self.mongo_client_dao = MongoDao()
        db = self.mongo_client_dao.client["Rewards"]
        self.collection = db["rewards"]

    def calculate_rewards(self, email, order_total):
        # Calculate the reward points
        reward_points = int(order_total)

        # Look up the reward tiers from MongoDB
        rewards = self.mongo.rewards.find().sort("points", pymongo.ASCENDING)

        # Determine the current reward tier and next reward tier
        current_reward_tier = None
        next_reward_tier = None
        for reward in rewards:
            if reward_points >= reward["points"]:
                current_reward_tier = reward
            else:
                next_reward_tier = reward
                break

        # If the customer has reached the highest reward tier, set the next reward tier to infinity
        if next_reward_tier is None:
            next_reward_tier = {"points": float("inf"), "tier": "", "rewardName": "", "discount": 0}

        # Calculate the rewards data
        rewards_data = {
            "email": email,
            "rewardPoints": reward_points,
            "rewardTier": current_reward_tier["tier"],
            "rewardTierName": current_reward_tier["rewardName"],
            "nextRewardTier": next_reward_tier["tier"],
            "nextRewardTierName": next_reward_tier["rewardName"],
            "nextRewardTierProgress": (next_reward_tier["points"] - reward_points) / (next_reward_tier["points"] - current_reward_tier["points"])
        }

        return rewards_data
