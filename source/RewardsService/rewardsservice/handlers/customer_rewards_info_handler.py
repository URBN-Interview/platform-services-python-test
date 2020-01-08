import tornado.web
import json

from pymongo import MongoClient

email = None
points = None


class CustomerInfoHandler(tornado.web.RequestHandler):
    """Gets customer email and order total from a form entry,"""
    """then calculates some other data points and adds them to DB"""

    def post(self):
        """Gets customer field input"""
        try:
            global email
            global points

            email = self.get_argument('order_email')
            points = float(self.get_argument('order_total'))
            points = int(points)

            # Customer can't exceed 1000 points
            if points > 1000:
                points = 1000

            self.get()
        except ValueError:
            self.write("A value error occurred")
        except NameError:
            self.write("Variable not found")
        except TypeError:
            self.write("A type error has occurred")
        except SystemError:
            self.write("A system error has occurred")
        except RuntimeError:
            self.write("Error retrieving data")

    def get(self):
        """Get the list of reward tiers from DB, manipulates/calculates rest of data and stores it in db"""
        try:
            global email
            global points

            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = db["customers"]
            rewards = db["rewards"]

            # find customer data if exists, add points if it does
            customer_found = customers.find_one({"email": email}, {"_id": 0})
            if customer_found is not None:
                points += customer_found["points"]
                if int(points) > 1000:
                    points = 1000

            # Round points down to find appropriate rewards tier
            tmp_points = int(points / 100) * 100

            # find appropriate rewards tier in collection and
            # Get data for the reward name and tier
            rewards_tier = rewards.find_one({"points": tmp_points}, {"_id": 0})
            rewardName = rewards_tier['rewardName']
            tier = rewards_tier['tier']

            # Get next tier data
            if points != 1000:
                nextTier = chr(ord(tier) + 1)
                y = rewards.find_one({"tier": nextTier}, {"_id": 0})
                nextRewardName = y['rewardName']
                nextPoints = y['points']
                nextTierProgression = str(int((points / nextPoints) * 100)) + "%"
            else:  # else the customer has reached the max tier
                nextRewardName = "N/A"
                nextTier = "N/A"
                nextTierProgression = "N/A"

            # Create customer info DB entry
            customer_info = {"email": email, "points": points, "tier": tier, "rewardName": rewardName,
                             "nextTier": nextTier, "nextRewardName": nextRewardName,
                             "nextTierProgression": nextTierProgression}
            # Insert customer info into Customer DB collection
            myQuery = {"email": email}  # Find previous entry and delete it
            customers.delete_one(myQuery)
            customers.insert_one(customer_info)
            return
        except KeyError:
            self.write("A key error occurred")
        except ValueError:
            self.write("A value error occurred")
        except NameError:
            self.write("Variable not found")
        except TypeError:
            self.write("A type error has occurred")
        except SystemError:
            self.write("A system error has occurred")
        except RuntimeError:
            self.write("Error inserting data")
