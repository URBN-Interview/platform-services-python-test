import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

import logging
logger = logging.getLogger(__name__)

class CustomerOrderHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            client = MongoClient("mongodb", 27017)

            db = client["Rewards"]
            rewards = db["rewards"]
            email = str(self.get_argument('email'))
            order_total = int(self.get_argument('total'))

            current_customer_reward = db.customer_rewards.find_one({"email":email},{"_id":0})
            if current_customer_reward:
                total_points = order_total + current_customer_reward["points"]
                customer_reward_data = self.get_customer_reward_data(email,total_points,rewards)
                db.customer_rewards.update(
                        {"email": email},
                        {
                            "$set": 
                            {
                                "points": customer_reward_data['points'],
                                "rewardTier": customer_reward_data['rewardTier'],
                                "rewardTierName":customer_reward_data['rewardTierName'],
                                "nextRewardTier": customer_reward_data['nextRewardTier'],
                                "nextRewardName": customer_reward_data['nextRewardName'],
                                "nextRewardTierProgress":customer_reward_data['nextRewardTierProgress']
                            }
                        },upsert=True)
                self.write('Reward info updated for customer with email address: {0} '.format(email))
            else:
                customer_reward_data = self.get_customer_reward_data(email,order_total,rewards)
                db.customer_rewards.insert_one(customer_reward_data)
                #all_rewards = list(db.customer_rewards.find({}, {"_id": 0}))
                self.write('Reward info inserted for customer with email address: {0} '.format(email))
        except ValueError as e:
            logger.info('ValueError: {0}'.format(e))
            self.write('An Error occured with Value type.')
        except RuntimeError as e:
            logger.info('RuntimeError: {0}'.format(e))
            self.write("A runtime error occured, please check database")
        except SystemError as e:
            logger.info('SystemError: {0}'.format(e))
            self.write("A error occured with the System.")
        
    def get_customer_reward_data(self,email,points,rewards):
        if points > 1000:
            points = 1000

        rounded_points = int(points/100) * 100
        reward_tier = rewards.find_one({"points":rounded_points},{"_id":0})

        if not reward_tier:
            reward_tier = {'points': 0, 'rewardName': 'No off for purchase', 'tier': 'no tier'}
        tier = reward_tier["tier"]
        reward_name = reward_tier["rewardName"]

        if points == 1000:
            next_reward_points = 'None'
            next_reward_name = 'None'
            next_reward_tier_progress = 'None'
            next_reward_tier = 'None'
        else:
            if tier == 'no tier':
                next_reward_tier = 'A'
            else:
                next_reward_tier = chr(ord(tier)+1)

            next_rewards_info = rewards.find_one({"tier":next_reward_tier},{"_id": 0})
            next_reward_points = next_rewards_info["points"]
            next_reward_name = next_rewards_info["rewardName"]
            next_reward_tier_progress = str(int((points / next_reward_points) * 100)) + '%'

        customer_reward_data = {"email": email, "points": points, "rewardTier":tier,
                                "rewardTierName": reward_name,"nextRewardTier": next_reward_tier, 
                                "nextRewardName": next_reward_name,
                                "nextRewardTierProgress": next_reward_tier_progress}

        return customer_reward_data

