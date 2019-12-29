import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerInfoHandler(tornado.web.RequestHandler):

    email = None
    points = None
    rewards_tier = None
    next_tier = None

    @staticmethod
    def create_dictionary(*args):
        return dict((k, eval(k)) for k in args)


    def post(self):
        """Gets customer field input"""
        try:
            CustomerInfoHandler.email = self.get_arguement("enter email address")
            tmp_points = self.get_arguement("enter order total")
            CustomerInfoHandler.points = int(tmp_points) # round down change

            # Customer can't exceed 1000 points
            if CustomerInfoHandler.points > 1000:
                CustomerInfoHandler.points = 1000
        except TyperError:
            print("A TypeError occurred")
        except:
            print("Error retrieving form data")


    def get(self):
        """Get the list of reward tiers from DB and find/store appropriate one"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            rewards = list(db.rewards.find({}, {"_id": 0}))
            found = False

            # Round points down to find appropriate rewards tier
            tmp_points = int(math.floor(CustomerInfoHandler.points / 100)) * 100

            # Find correct rewards tier via points
            for x in rewards:
                for key, value in x.iteritems():
                    if key == 'points' and value == tmp_points:
                        CustomerInfoHandler.rewards_tier = x
                        found = True
                    elif found is True:
                        CustomerInfoHandler.next_tier = x
                        break
                if found is True:
                    break
        except TyperError:
            print("A TypeError occurred")
        except:
            print("Error finding correct tier")


    def put(self):
        """Use data gathered above to input customer reward data into DB"""
        try:
            for key, value in CustomerInfoHandler.rewards_tier:     # For loop to get reward name and tier name
                if key == 'rewardName':
                    rewardName = value
                elif key == 'tier':
                    tier = value

            # If customers points are less than 1000:
            # for loop to get next reward name, next tier name, and next points
            if points != 1000:
                for key, value in CustomerInfoHandler.next_tier:
                    if key == 'rewardName':
                        nextRewardName = value
                    elif key == 'tier':
                        nextTier = value
                    elif key == 'points':
                        nextPoints = value
                    nextTierProgression = int((CustomerInfoHandler.points / nextPoints) * 100)
            else:                               # else the customer has reached the max tier
                nextRewardName = "N/A"
                nextTier = "N/A"
                nextTierProgression = "N/A"

            # Create customer info DB entry
            customer_info = self.create_dictionary(CustomerInfoHandler.email, CustomerInfoHandler.points, tier,
                                                   rewardName,nextTier, nextRewardName, nextTierProgression)

            # Insert customer info into Customer DB collection
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            coll = db["Customers"]
            coll.insert_one(customer_info)

        except TyperError:
            print("A TypeError occurred")
        except:
            print("Error finding correct tier")
