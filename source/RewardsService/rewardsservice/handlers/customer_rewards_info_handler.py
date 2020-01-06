import tornado.web
import math
import pymongo


class CustomerInfoHandler(tornado.web.RequestHandler):
    """Gets customer email and order total from a form entry,"""
    """then calculates some other data points and adds them to DB"""

    email = None
    points = None
    rewards_tier = None

    @staticmethod
    def create_dictionary(*args):
        return dict((k, eval(k)) for k in args)

    def post(self):
        """Gets customer field input"""
        try:
            CustomerInfoHandler.email = self.get_arguement('order_email')
            tmp_points = self.get_arguement('order_total')
            CustomerInfoHandler.points = int(tmp_points)  # round down change

            # Customer can't exceed 1000 points
            if CustomerInfoHandler.points > 1000:
                CustomerInfoHandler.points = 1000
        except:
            print("Error retrieving form data")

    def get(self):
        """Get the list of reward tiers from DB and find/store appropriate one"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = db["customers"]
            rewards = db["rewards"]

            # find customer data if exists, add points if it does
            customer_found = customers.find({"email": CustomerInfoHandler.email}, {"_id": 0})
            if customer_found is not None:
                x = json.loads(customer_found)
                CustomerInfoHandler.points += x["points"]
                if CustomerInfoHandler.points > 1000:
                    CustomerInfoHandler.points = 1000

            # Round points down to find appropriate rewards tier
            tmp_points = int(math.floor(CustomerInfoHandler.points / 100)) * 100

            # find appropriate rewards tier in collection
            CustomerInfoHandler.rewards_tier = rewards.find({"points": tmp_points}, {"_id": 0})
        except:
            print("Error finding correct tier")

    def put(self):
        """Use data gathered above to input customer reward data into DB"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = db["customers"]

            # Get data for the reward name and tier
            x = json.loads(CustomerInfoHandler.rewards_tier)
            rewardName = x["rewardName"]
            tier = x["tier"]

            # Get next tier data
            if CustomerInfoHandler.points != 1000:
                nextTier = chr(ord(tier) + 1)
                y = json.loads(customers.find({"tier": nextTier}))
                nextRewardName = y["rewardName"]
                nextPoints = y["nextPoints"]
                nextTierProgression = str(int((CustomerInfoHandler.points / nextPoints) * 100)) + "%"
            else:  # else the customer has reached the max tier
                nextRewardName = "N/A"
                nextTier = "N/A"
                nextTierProgression = "N/A"

            # Create customer info DB entry
            email = CustomerInfoHandler.email
            points = CustomerInfoHandler.points
            customer_info = self.create_dictionary(email, points, tier,
                                                   rewardName, nextTier, nextRewardName, nextTierProgression)

            # Insert customer info into Customer DB collection
            myQuery = self.create_dictionary(email)  # Find previous entry and delete it
            coll.delete_one(myQuery)
            coll.insert_one(customer_info)

        except:
            print("Error inserting customer info")
