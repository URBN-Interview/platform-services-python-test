import json
from bson import json_util
import tornado.web
from tornado.escape import json_decode
import math
from pymongo import MongoClient, ReturnDocument
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):

    # this get function will parse the request body that comes from the front end, it will use a handler that will seek the entry in mongoDB and then return the result
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        req_data = json_decode(self.request.body)
        document = db.customers.find_one(
            {"email": req_data["email"]}, {"_id": 0})
        # json.dumps would not parse this because it was ObjectId
        self.write(json_util.dumps(document))

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        req_data = json_decode(self.request.body)
        PurchasePoints = math.floor(req_data["cost"])
        # increment points and get an updated mongo doc to work with
        document = db.customers.find_one_and_update(
            {"email": req_data["email"]},
            {"$inc": {"points": PurchasePoints}},
            upsert=True,
            return_document=ReturnDocument.AFTER)

        # find relevant tiers relative to current level
        CurrentLevel = (math.floor(document["points"]/100) * 100)
        RelevantTiers = list(db.rewards.find(
            {"points": {"$gte": CurrentLevel}}))

        # create update object for rewards information
        update = {
            "tier": None,
            "rewardName": None,
            "nextTier": "A",
            "nextTierRewardName": "5% off purchase",
            "nextTierProgress": None
        }
        if document["points"] < 100:
            ###
            # See Engineering note 1 in log.md
            ###
            update["nextTierProgress"] = str(
                document["points"] - (math.floor(document["points"]/100)*100)) + "%"
        elif document["points"] < 1000:
            update["tier"] = RelevantTiers[0]["tier"]
            update["rewardName"] = RelevantTiers[0]["rewardName"]
            update["nextTier"] = RelevantTiers[1]["tier"]
            update["nextTierRewardName"] = RelevantTiers[1]["rewardName"]
            update["nextTierProgress"] = str(
                document["points"] - (math.floor(document["points"]/100)*100)) + "%"
        else:
            update["tier"] = "J"
            update["rewardName"] = "50% off purchase"
            update["nextTier"] = "You have reached the highest tier!!! You're my hero!!!"
            update["nextTierRewardName"] = "You have the highest rewards tier at 50% off!!!"
            update["nextTierProgress"] = "100%"

        # finally we update the record with these calculated details

        fullDocument = db.customers.find_one_and_update(
            {"email": req_data["email"]},
            {"$set": update},
            return_document=ReturnDocument.AFTER)

        thankYouMessage = "Thank you for your purchase " + \
            fullDocument["email"] + \
            "!!!!! Your new point total is " + \
            str(fullDocument["points"]) + " points!!!"
        self.write(thankYouMessage)
