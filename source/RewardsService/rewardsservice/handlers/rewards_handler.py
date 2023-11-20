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


def calculate_reward_tier(reward_points, reward_tiers):
    reward_tier = None
    reward_tier_name = None
    next_reward_tier = None
    next_reward_tier_name = None
    next_reward_tier_progress = None

    for tier_data in reward_tiers:
        if reward_points >= tier_data["points"]:
            reward_tier = tier_data["tier"]
            reward_tier_name = tier_data["rewardName"]
        else:
            next_reward_tier = "A"
            next_reward_tier_name = "5% off purchase"
            next_reward_tier_progress = round(((100 - reward_points) / 100), 3)

    if reward_tier:
        next_tier_index = ord(reward_tier) - ord("A") + 1
        if next_tier_index < len(reward_tiers):
            next_reward_tier_data = reward_tiers[next_tier_index]
            next_reward_tier = next_reward_tier_data["tier"]
            next_reward_tier_name = next_reward_tier_data["rewardName"]
            points_needed = next_reward_tier_data["points"]
            next_reward_tier_progress = round(((points_needed - reward_points) / points_needed), 3)

    return (
        reward_tier,
        reward_tier_name,
        next_reward_tier,
        next_reward_tier_name,
        next_reward_tier_progress,
    )

def update_customer_rewards(db, email, reward_points, reward_tiers):
    existing_customer = db.customer_rewards.find_one({"email": email})

    if existing_customer:
        existing_reward_points = existing_customer.get("reward_points", 0)
        updated_reward_points = existing_reward_points + reward_points

        (
            reward_tier,
            reward_tier_name,
            next_reward_tier,
            next_reward_tier_name,
            next_reward_tier_progress,
        ) = calculate_reward_tier(updated_reward_points, reward_tiers)

        db.customer_rewards.update_one(
            {"email": email},
            {
                "$set": {
                    "reward_points": updated_reward_points,
                    "reward_tier": reward_tier,
                    "reward_tier_name": reward_tier_name,
                    "next_reward_tier": next_reward_tier,
                    "next_reward_tier_name": next_reward_tier_name,
                    "next_reward_tier_progress": next_reward_tier_progress,
                }
            },
        )
        return "Reward points updated successfully."
    else:
        (
            reward_tier,
            reward_tier_name,
            next_reward_tier,
            next_reward_tier_name,
            next_reward_tier_progress,
        ) = calculate_reward_tier(reward_points, reward_tiers)

        db.customer_rewards.insert(
            {
                "email": email,
                "reward_points": reward_points,
                "reward_tier": reward_tier,
                "reward_tier_name": reward_tier_name,
                "next_reward_tier": next_reward_tier,
                "next_reward_tier_name": next_reward_tier_name,
                "next_reward_tier_progress": next_reward_tier_progress,
            }
        )
        return "Order data stored successfully."

def validate_and_update_rewards(self, email, order_total, reward_tiers):
        if not validate_email(email):
            return "Invalid email format. Please provide a valid email address."
        elif not order_total.replace(".", "", 1).isdigit():
            return "Invalid order total. Please provide a valid number."

        reward_points = int(float(order_total))
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        return update_customer_rewards(db, email, reward_points, reward_tiers)



class RewardsHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        email = self.get_argument("email")
        order_total = self.get_argument("order_total")
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        reward_tiers=list(db.rewards.find({}))
        
        response_message = validate_and_update_rewards(self, email, order_total, reward_tiers)
        self.write(json.dumps(response_message))

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
    