import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))



class RewardPointsHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            # Extract data from request
            email = self.get_body_argument("email")
            order_total = float(self.get_body_argument("order_total"))

            # Calculate rewards data
            reward_points = int(order_total)
            reward_tier = chr((reward_points // 100) + 65)  # Convert points to tier using ASCII
            reward_tier_name = f"{reward_points}% off purchase"
            next_reward_tier = chr((reward_points // 100) + 66) if reward_points // 100 < 5 else None
            next_reward_tier_name = f"{(reward_points + 100)}% off purchase" if next_reward_tier else None
            next_reward_tier_progress = (reward_points % 100) / 100 if next_reward_tier else None

            # Store data in MongoDB
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            collection = db["reward_data"]
            customer_data = {
                "email": email,
                "reward_points": reward_points,
                "reward_tier": reward_tier,
                "reward_tier_name": reward_tier_name,
                "next_reward_tier": next_reward_tier,
                "next_reward_tier_name": next_reward_tier_name,
                "next_reward_tier_progress": next_reward_tier_progress
            }
            result = collection.insert_one(customer_data)

            # Response
            self.set_status(201)
            self.write({"message": "Reward data stored successfully.", "customer_id": str(result.inserted_id)})

        except tornado.web.MissingArgumentError as e:
            # Handle missing argument error
            self.set_status(400)
            self.write({"error": "Missing argument.", "message": str(e)})
        except ValueError as e:
            # Handle value conversion error
            self.set_status(400)
            self.write({"error": "Invalid value.", "message": str(e)})
        except Exception as e:
            # Handle other exceptions
            self.set_status(500)
            self.write({"error": "Internal server error.", "message": str(e)})
