import json
from bson import json_util
import tornado.web
from tornado.escape import json_decode
import math
from pymongo import MongoClient, ReturnDocument
from tornado.gen import coroutine
from handlers.handler_util import processDocument


class CustomerHandler(tornado.web.RequestHandler):

    # this get function will parse the request body that comes from the front end, it will use a handler that will seek the entry in mongoDB and then return the result
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        req_data = json_decode(self.request.body)
        document = db.customers.find_one(
            {"email": req_data["email"]}, {"_id": 0})

        # handle bad lookup
        if not document:
            document = {
                "email": "Invalid Email",
                "points": "N/A",
                "tier": "N/A",
                "rewardName": "N/A",
                "nextTier": "N/A",
                "nextTierRewardName": "N/A",
                "nextTierProgress": "N/A"
            }
        self.write(json.dumps([document]))

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

        update = processDocument(document, RelevantTiers)

        # finally we update the record with these calculated details

        fullDocument = db.customers.find_one_and_update(
            {"email": req_data["email"]},
            {"$set": update},
            return_document=ReturnDocument.AFTER)

        self.write(json_util.dumps(fullDocument))
