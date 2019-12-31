import tornado.web
import math

from pymongo import MongoClient


class CustomerInfoHandler(tornado.web.RequestHandler):
    """Gets customer email and order total from a form entry,"""
    """then calculates some other data points and adds them to DB"""

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
            CustomerInfoHandler.email = self.get_arguement('order_email')
            tmp_points = self.get_arguement('order_total')
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
            customers = list(db.customers.find({}, {"_id": 0}))
            tier_found = False
            next_tier_found = False
            email_found = False

            # Checks if customer already exists in Rewards DB and if so adds their points to this order total
            # Once, customer email is found, it continues onto next inner loop (next key) and adds the pre-existing points
            for y in customers:
                for key, value in y.iteritems():
                    if key == 'email' and value == CustomerInfoHandler.email:
                        email_found = True
                        continue
                    if email_found is True:
                        CustomerInfoHandler.points += value
                        break
                if email_found is True:
                    break

            # Round points down to find appropriate rewards tier
            tmp_points = int(math.floor(CustomerInfoHandler.points / 100)) * 100

            # Find correct rewards tier via points
            # Loops through tiers to find correct one, and breaks out of inner loop if found
            # On next loop of tiers, it sets the next_tier value and breaks out of inner loop
            # and with both found, the if statement breaks out of outer loop
            for x in rewards:
                for key, value in x.iteritems():
                    if key == 'points' and value == tmp_points:
                        CustomerInfoHandler.rewards_tier = x
                        tier_found = True
                        break
                    elif tier_found is True:
                        CustomerInfoHandler.next_tier = x
                        next_tier_found = True
                        break
                if tier_found is True and next_tier_found is True:       # Break outer loop if correct info found
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
            if CustomerInfoHandler.points != 1000:
                for key, value in CustomerInfoHandler.next_tier:
                    if key == 'rewardName':
                        nextRewardName = value
                    elif key == 'tier':
                        nextTier = value
                    elif key == 'points':
                        nextPoints = value
                    nextTierProgression = str(int((CustomerInfoHandler.points / nextPoints) * 100)) + "%"
            else:                               # else the customer has reached the max tier
                nextRewardName = "N/A"
                nextTier = "N/A"
                nextTierProgression = "N/A"

            # Create customer info DB entry
            email = CustomerInfoHandler.email
            points = CustomerInfoHandler.points
            customer_info = self.create_dictionary(email, points, tier,
                                                   rewardName,nextTier, nextRewardName, nextTierProgression)

            # Insert customer info into Customer DB collection
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            coll = db["customers"]
            myquery = self.create_dictionary(email)     # Find previous entry and delete it
            coll.delete_one(myquery)
            coll.insert_one(customer_info)

        except TyperError:
            print("A TypeError occurred")
        except:
            print("Error inserting customer info")
