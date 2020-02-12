import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from utils import is_email_valid

import logging
logger = logging.getLogger(__name__)

class CustomerOrderHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        try:
            client = MongoClient("mongodb", 27017)

            db = client["Rewards"]
            rewards = db["rewards"]
            email = str(self.get_argument('email'))
            order_total = float(self.get_argument('total'))
            '''
            if not email or not is_email_valid(email):
                raise ValueError(' email not valid, email: {0}'.format(email))
            '''
            # grab customer info if email exist, update the record,
            # other wise insert a new record for the email
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
                                "nextRewardTierName": customer_reward_data['nextRewardTierName'],
                                "nextRewardTierProgress":customer_reward_data['nextRewardTierProgress']
                            }
                        },upsert=True)

                self.write({
                            "status": 200,
                            "message": "Reward info udated for customer.",
                            "details": {"email": email}
                            })
            else:
                customer_reward_data = self.get_customer_reward_data(email,order_total,rewards)
                db.customer_rewards.insert_one(customer_reward_data)

                self.write({
                            "status": 200,
                            "message": "Reward info inserted for customer.",
                            "details": {"email": email}
                            })
        except ValueError as e:
            logger.info('ValueError: {0}'.format(e))
            self.write('An Value type error occured,an vaild email and order total are needed. Error:{0}'.format(e))
        except RuntimeError as e:
            logger.info('RuntimeError: {0}'.format(e))
            self.write("A runtime error occured, please check database.Error:{0}".format(e))
        except SystemError as e:
            logger.info('SystemError: {0}'.format(e))
            self.write("A error occured with the System.Error:{0}".format(e))

    # get the customer tier base on the point
    def get_customer_reward_data(self,email,points,rewards):
        # if point is higher than 1000,set point to 1000
        original_points = points
        if points > 1000:
            points = 1000

        # perform calculating to round the number, ex: 290 would give 200
        # this helps us determine the bottom tier range a customer belong to.
        # if a customer has 290 point then, we know that they belong at the 200 points group
        rounded_points = int(points/100) * 100
        reward_tier = rewards.find_one({"points":rounded_points},{"_id":0})

        # if the customer has point fewer than 100, then they belong at no tier
        # set up a temperary tier, so that we can use that info later
        if not reward_tier:
            reward_tier = {'points': 0, 'rewardName': 'No off for purchase', 'tier': 'no tier'}
        tier = reward_tier["tier"]
        reward_name = reward_tier["rewardName"]

        # if the customer reached the highest tier, then their next tier info are set to None
        if points == 1000:
            next_reward_points = 'None'
            next_reward_tier_name = 'None'
            next_reward_tier_progress = 'None'
            next_reward_tier = 'None'
        else:
            # use alphabet to get the next tier, 
            # if there is no current tier, then we know the next tier would be A
            if tier == 'no tier':
                next_reward_tier = 'A'
            else:
                next_reward_tier = chr(ord(tier)+1)

            next_rewards_info = rewards.find_one({"tier":next_reward_tier},{"_id": 0})
            next_reward_points = next_rewards_info["points"]
            next_reward_tier_name = next_rewards_info["rewardName"]

            #calculate the progression bease on current point and next reward points
            next_reward_tier_progress = str(int((points / next_reward_points) * 100)) + '%'

        customer_reward_data = {"email": email, "points": original_points, "rewardTier":tier,
                                "rewardTierName": reward_name,"nextRewardTier": next_reward_tier, 
                                "nextRewardTierName": next_reward_tier_name,
                                "nextRewardTierProgress": next_reward_tier_progress}

        return customer_reward_data

