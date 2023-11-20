import json
import tornado.web


from pymongo import MongoClient
from tornado.gen import coroutine

################## Function to validate email format ####################
import re

def validate_email(email):
    # Regular expression for email validation
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_pattern, email) is not None


#########################################################################



class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        #Endpoint 1
        email = self.get_argument("email")
        order_total = self.get_argument("order_total")

         # Check whether the email is valid or not
        if not validate_email(email):
            self.write(json.dumps("Invalid email format. Please provide a valid email address."))

        #  Check whether the given order_total value is valid numeric value or not
        elif not order_total.replace(".", "", 1).isdigit():
            self.write(json.dumps("Invalid order total. Please provide a valid number."))
        else:
            # Calculate reward points based on order total (1 point per dollar)
            reward_points = int(order_total)

            # Logic to determine Reward Tier, Reward Tier Name, Next Reward Tier, Next Reward Tier Name, Next Reward Tier Progress

            reward_tiers = [
                {"tier": "A", "rewardName": "5% off purchase", "points": 100},
                {"tier": "B", "rewardName": "10% off purchase", "points": 200},
                {"tier": "C", "rewardName": "15% off purchase", "points": 300},
                {"tier": "D", "rewardName": "20% off purchase", "points": 400},
                {"tier": "E", "rewardName": "25% off purchase", "points": 500},
                {"tier": "F", "rewardName": "30% off purchase", "points": 600},
                {"tier": "G", "rewardName": "35% off purchase", "points": 700},
                {"tier": "H", "rewardName": "40% off purchase", "points": 800},
                {"tier": "I", "rewardName": "45% off purchase", "points": 900},
                {"tier": "J", "rewardName": "50% off purchase", "points": 1000}
            ]
            
            # Find the reward tier for the customer based on their earned points
            reward_tier = None
            reward_tier_name = None
            next_reward_tier = None
            next_reward_tier_name = None
            next_reward_tier_progress = None

            # for tier_data in reward_tiers:
            #     if reward_points >= tier_data["points"]:
            #         reward_tier = tier_data["tier"]
            #         reward_tier_name = tier_data["rewardName"]
            #     else:
            #         next_reward_tier = "A"
            #         next_reward_tier_name = "5% off purchase"
            #         next_reward_tier_progress = round(((100 - reward_points) / 100),2)

            # # Find next reward tier details if applicable
            # if reward_tier:
            #     next_tier_index = ord(reward_tier) - ord("A") + 1
            #     if next_tier_index < len(reward_tiers):
            #         next_reward_tier_data = reward_tiers[next_tier_index]
            #         next_reward_tier = next_reward_tier_data["tier"]
            #         next_reward_tier_name = next_reward_tier_data["rewardName"]
            #         points_needed = next_reward_tier_data["points"]
            #         next_reward_tier_progress = round(((points_needed - reward_points) / points_needed),2)


            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]

            # Check if the email already exists in the database
            existing_customer = db.customer_rewards.find_one({"email": email})

            if existing_customer:
                # Add new reward points to the existing reward_points
                existing_reward_points = existing_customer.get("reward_points", 0)
                updated_reward_points = existing_reward_points + reward_points

                for tier_data in reward_tiers:
                    if updated_reward_points >= tier_data["points"]:
                        reward_tier = tier_data["tier"]
                        reward_tier_name = tier_data["rewardName"]
                    else:
                        next_reward_tier = "A"
                        next_reward_tier_name = "5% off purchase"
                        next_reward_tier_progress = round(((100 - updated_reward_points) / 100),3)

                # Find next reward tier details if applicable
                if reward_tier:
                    next_tier_index = ord(reward_tier) - ord("A") + 1
                    if next_tier_index < len(reward_tiers):
                        next_reward_tier_data = reward_tiers[next_tier_index]
                        next_reward_tier = next_reward_tier_data["tier"]
                        next_reward_tier_name = next_reward_tier_data["rewardName"]
                        points_needed = next_reward_tier_data["points"]
                        next_reward_tier_progress = round(((points_needed - updated_reward_points) / points_needed),3)

                # Update existing entry with updated reward points
                db.customer_rewards.update_one(
                    {"email": email},
                    {"$set": {
                        "reward_points": updated_reward_points,
                        "reward_tier": reward_tier,
                        "reward_tier_name": reward_tier_name,
                        "next_reward_tier": next_reward_tier,
                        "next_reward_tier_name": next_reward_tier_name,
                        "next_reward_tier_progress": next_reward_tier_progress
                    }}
                )
                self.write(json.dumps("Reward points updated successfully."))
            else:
                for tier_data in reward_tiers:
                    if reward_points >= tier_data["points"]:
                        reward_tier = tier_data["tier"]
                        reward_tier_name = tier_data["rewardName"]
                    else:
                        next_reward_tier = "A"
                        next_reward_tier_name = "5% off purchase"
                        next_reward_tier_progress = round(((100 - reward_points) / 100),3)

                # Find next reward tier details if applicable
                if reward_tier:
                    next_tier_index = ord(reward_tier) - ord("A") + 1
                    if next_tier_index < len(reward_tiers):
                        next_reward_tier_data = reward_tiers[next_tier_index]
                        next_reward_tier = next_reward_tier_data["tier"]
                        next_reward_tier_name = next_reward_tier_data["rewardName"]
                        points_needed = next_reward_tier_data["points"]
                        next_reward_tier_progress = round(((points_needed - reward_points) / points_needed),3)

                db.customer_rewards.insert({
                    "email": email,
                    "reward_points": reward_points,
                    "reward_tier": reward_tier,
                    "reward_tier_name": reward_tier_name,
                    "next_reward_tier": next_reward_tier,
                    "next_reward_tier_name": next_reward_tier_name,
                    "next_reward_tier_progress": next_reward_tier_progress
                })
            #self.write("Customer rewards data stored successfully.")
            self.write(json.dumps("Order data stored succesfully"))


    def get(self):
        # Get the requested URL
        endpoint = self.request.path
        #Endpoint 2
        if endpoint == '/user/rewards':
            email_to_find = self.get_argument("email")
             # Validate email format
            if not validate_email(email_to_find):
                self.write(json.dumps("Invalid email format. Please provide a valid email address."))
            else:
                # Retrieve customer's rewards data from MongoDB based on the email
                client = MongoClient("mongodb", 27017)
                db = client["Rewards"]
                customer_data = list(db.customer_rewards.find({"email": email_to_find}, {"_id": 0}))

                # Return the customer's rewards data
                if customer_data:                    
                    self.write(json.dumps(customer_data))
                else:
                    self.write(json.dumps("Customer data not found."))
        #Endpoint 3
        elif endpoint == '/allcustomers/rewards':
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customer_rewards = list(db.customer_rewards.find({}, {"_id": 0}))
            self.write(json.dumps(customer_rewards))

        #Rewards Tiers
        elif endpoint == '/rewards':
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            rewards = list(db.rewards.find({}, {"_id": 0}))
            self.write(json.dumps(rewards))
    