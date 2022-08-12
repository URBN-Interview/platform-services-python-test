import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))

class EndPointOne(tornado.web.RequestHandler):
    """post or put for user
    1. database should already be created
    2. get should show form
    3. post should put data into database"""
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("endpoint_one.html", title="My title", items=items)
    
    def post(self):
        self.write(self.__class__.__name__)

class EndPointTwo(tornado.web.RequestHandler):
    """get user info"""
    def get(self):
        self.write(self.__class__.__name__)

class EndPointThree(tornado.web.RequestHandler):
    """Get all user Info"""
    def get(self):
        self.write(self.__class__.__name__)