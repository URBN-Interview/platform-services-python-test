import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from handlers.base import BaseHandler
from http import HTTPStatus

class RewardsHandler(BaseHandler):
    
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        #self.write(json.dumps(rewards,indent='\t'))
        self.write_response(status_code=HTTPStatus.OK.value,
                                    result=rewards)