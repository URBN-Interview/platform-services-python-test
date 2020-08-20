import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class RewardsHandler(tornado.web.RequestHandler):
	
	@coroutine
	def get(self):
		client = MongoClient("mongodb", 27017)
		db = client["Rewards"]
		db = client["Customers"]
		rewards = list(db.rewards.find({}, {"_id": 0}))
		self.write(json.dumps(db.rewards.distinct("tier")))


















