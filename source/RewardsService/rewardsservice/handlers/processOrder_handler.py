import json
import tornado.web
import sys
from pymongo import MongoClient
from tornado.gen import coroutine

#could've used this (bisect_left on the nxn array's points to find entry) to generate a 2-d array; decided against it as the assignment doesn't say the values will be changed
#Tradeoff: Development pace for flexibility
#sys.path.append("..")
# from rewardsConfig import tierInformation

class ProcessOrderHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        self.write('<html><body><form action="/processOrder/" method="POST">'
                    '<p1>Use This Form to send the post req or send req directly</p1><br>'
                   '<p1>email</p1> <input type="text" name="email">'
                   '<p1>order_total</p1> <input type="text" name="order_total">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
        
    """ ProcessOrderHandler
    POST:
        summary: Accepts a customer's order data: email adress (string) and order total (float).
        description: returns None
        url: /processOrder
        parameters:
            - email adress (string)
            - order total (float)
        responses:
            200:
                Incomplete/Incorrect parameters
            404:
                Connection error with DB or python error
    """
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        
        #list the collections available in db
        print(db.list_collection_names())
        #Select Customers collection; create if doesn't exist (1st call)
        col = db["Customers"]
        
        #process arguments
        orderTotal = float(self.get_arguments("order_total")[0])
        email = self.get_arguments("email")[0]

        print('orderArg: {}'.format(orderTotal))
        print('emailArg: {}'.format(email))
        cursor = col.find({"email": email})
        matches = list(cursor)
        print(matches)

        resultArr = generateUpdate(matches, orderTotal, email)
        print(resultArr)
        if len(matches)==0:
            # data = json.loads(bson.json_util.dumps(resultArr)) #don't want to introduce dependency
            col.insert(resultArr)
        else:
            newvalues = { "$set": resultArr }
            col.update_one(matches[0], newvalues)
        self.write(resultArr if len(matches)!=0 else self.encode(resultArr))

    def encode(self, o):
            if '_id' in o:
                o['_id'] = str(o['_id'])
            return o

"""
Accepts matches, email/total of a user then returns updated list to feed in db
"""
def generateUpdate(matches, orderTotal, email):
    print("orderToll: {}".format(orderTotal))
    points = int(orderTotal/1)
    print(points)
    if len(matches)==0:
        #TODO handle case of no user exists
        print('no user found!')
    else:
        #TODO: handle case of a matched user
        data = matches[0]
        print('user found! {}'.format(data))
        oldPoints = data["reward_points"]
        points+=oldPoints
        print("stored points {}".format(oldPoints))
    rewardTier,tierName,nextTier,nextTierName,nextTierProgress = getTierInformation(points)
    return {"email":email, "reward_points": points,"reward_tier": rewardTier,"reward_tier_name": tierName,"next_reward_tier": nextTier,"next_reward_tier_name": nextTierName,"next_reward_progress": nextTierProgress}
"""
Accepts points, returns (rewardTier, tierName, nextTier, nextTierName, nextTierProgress)
"""
def getTierInformation(points):
    tierDiff = 100
    tierIndex = 0 if points<100 else min(10, points//100)
    print("tierIndex: {}".format(tierIndex))
    rewardTier = chr(ord('A')+ (tierIndex-1)) if tierIndex!=0 else ''
    tierName = str(5*tierIndex) + "% off purchase"
    nextTier = "A" if rewardTier=='' else min('J', chr(ord(rewardTier)+1))
    nextTierName = str(5*min(10,(tierIndex+1))) + "% off purchase"
    nextTierProgress = (100-points%100) if tierIndex<10 else 0

    return rewardTier,tierName,nextTier,nextTierName,nextTierProgress

