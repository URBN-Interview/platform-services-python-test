import json
import tornado.web

import unittest, os, os.path, sys, urllib
from tornado.testing import AsyncHTTPTestCase

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
class RewardCalHandler(tornado.web.RequestHandler):

    def post(self, email, orderTotal):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
        except: 
            print("Connection failed")    
        rewardPoint = int(orderTotal)
        doc = db.rewards.find({"point": str(rewardPoint)})
        rewardTier = doc["tier"]
        tierName = doc["rewardName"]
        if doc[point] <= 900 :
            nextP = rewardPoint + 100
            nextdoc = db.rewards.find({"point": str(nextP)})
            nextTier = nextdoc["tier"]
            nextName = nextdoc["rewardName"]
            tierProgress = (nextP - rewardPoint)/rewardPoint # seems a constant
        else:
            nextP = rewardPoint + 100
            nextdoc = db.rewards.find({"point": str(nextP)})
            nextTier = None
            nextName = None
            tierProgress = 0 # seems a constant
        data = {"email": email,
                "rewardpoint": rewardPoint,
                "reward tier": rewardTier,
                "reward tier Name" : tierName,
                "next tier" : nextTier,
                "next tier name" : nextName, 
                "tier progress" : tierProgress
        }
        db.rewards.insert(data)

class RewardDetailHandler(tornado.web.RequestHandler):

    def get(self, email):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
        except:
            print("connection failed")   

        data = db.rewards.find({email : email}, {"_id": 0}) 
        self.write(json.dump(data))  

class AllDetailHandler(tornado.web.RequestHandler):

    def get(self):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
        except:
            print("connection failed")   

        data = db.rewards.find({email : email}, {"_id": 0}) 
        self.write(json.dump(data)) 
        
class TestHandler(AsyncHTTPTestCase):
    
    def create_something_test(self):

        post_args = {'email': 'bro@bro.com',
                     'orderTotal': 100
        }

        response = self.fetch(
            '/addreward',
            method='POST',
            body=urllib.urlencode(post_args),
            follow_redirects=False)
        self.assertEqual(response.code, 200)        
