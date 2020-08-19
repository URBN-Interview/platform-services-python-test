import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerRewardsHandler(tornado.web.RequestHandler):

	@coroutine
	def get(self):
		client = MongoClient("mongodb", 27017)
		db = client["Customers"]
		email_address = self.get_argument('emailAddress')
		customer_email_result = list(db.customers.find({"emailAddress": email_address}, {"_id":0}))
		self.write(json.dumps(customer_email_result))

	@coroutine
	def post(self):
		client = MongoClient("mongodb", 27017)
		db = client["Customers"]
		email_address = self.get_argument('emailAddress')
		order_total = float(self.get_argument('orderTotal'))

		#TODO: validate email and order total

		# if email adress was given and the order total was not negative
		if email_address and order_total >= 0:
			# check if customer with given email exists
			result = list(db.customers.find({"emailAddress": email_address}, {"_id":0}))

			# add new customer to db
			if not result:
				reward_points = math.floor(order_total)
				reward_tier_info = self.get_reward_tier_info(self.round_reward_value(reward_points))
				next_reward_tier_info = self.get_reward_tier_info(self.round_reward_value(reward_points) + 100)
				tier_progress = self.get_reward_tier_progress(reward_points, next_reward_tier_info[2])
				db.customers.insert({
					"emailAddress": email_address, 
					"rewardPoints": reward_points,
					"rewardTier":reward_tier_info[0],
					"rewardTierName":reward_tier_info[1],
					"nextRewardTier":next_reward_tier_info[0],
					"nextRewardTierName":next_reward_tier_info[1],
					"nextRewardTierProgress":tier_progress})

			# customer exists, grab result from list
			else:
				customer = result[0]
				reward_points = float(customer["rewardPoints"]) + math.floor(order_total)
				reward_tier_info = self.get_reward_tier_info(self.round_reward_value(reward_points))
				next_reward_tier_info = self.get_reward_tier_info(self.round_reward_value(reward_points) + 100)
				tier_progress = self.get_reward_tier_progress(reward_points, next_reward_tier_info[2])
				db.customers.replace_one({"emailAddress": email_address}, {
					"emailAddress": email_address, 
					"rewardPoints": reward_points, 
					"rewardTier":reward_tier_info[0], 
					"rewardTierName":reward_tier_info[1], 
					"nextRewardTier":next_reward_tier_info[0], 
					"nextRewardTierName":next_reward_tier_info[1], 
					"nextRewardTierProgress":tier_progress})

	'''
		Return a reward tier value in increments of 100 from 0 to 1000
	'''
	@staticmethod
	def round_reward_value(reward_points):
		if reward_points >= 1000: 
			return 1000
		multiplier = math.floor(reward_points / 100)
		return multiplier * 100

	'''
		Return tier info for a given tier, will return no reward tier for 0 points
	'''
	def get_reward_tier_info(self, current_tier_points):
		client = MongoClient("mongodb", 27017)
		db = client["Rewards"]

		# if the current tier points is 0, return no rewards available
		if current_tier_points == 0:
			return ["None", "No rewards available", 0]
		#if the current tier is greater or equal to 1000 points, get the 1000 point tier
		elif current_tier_points > 1000:
			return ["None", "No more rewards available", 0]

		# check if tier with points exits
		result = list(db.rewards.find({"points": current_tier_points}, {"_id":0}))

		# the tier passed in does not exist
		if not result:
			return ["None", "No rewards available", 0]
		# the tier is found
		else:
			tier = result[0]
			tier_value = tier["tier"]
			tier_reward = tier["rewardName"]
			tier_points = tier["points"]
			return [tier_value, tier_reward, tier_points]

	'''
		Return progress from 0 to 1, any progress over the tier (i.e. 1000 points) will return 1 or 100%
	'''
	@staticmethod
	def get_reward_tier_progress(reward_points, next_tier_points):
		multiplier = math.floor(reward_points / 100)
		if multiplier >= 10:
			return 1
		progress = (reward_points - multiplier * 100) / (next_tier_points - multiplier * 100)
		return progress