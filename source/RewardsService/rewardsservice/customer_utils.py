 #TO DO util funcs: 
    # is_email: Validate email as email
    # to_reward_points: convert orderTotal to reward points 
    # get_next_tier: calcuate percent to next tier, next tier and name 
import json
import tornado.web
import re

from pymongo import MongoClient
from tornado.gen import coroutine


def to_reward_points(orderTotal):
    points = math.floor(orderTotal)
    print("points", points)
    return points



def is_email_valid(email):
    reg = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
    
    if not re.match(reg, email):
        return false
    else:
        return true



@coroutine
def get_tier(points, email):
    client = MongoClient("mongodb", 27017)
    db = client["Rewards"]
    rewards = list(db.rewards.find({}, {"_id": 0}))

    if rewards < 100:
        progress = get_percent(points, 0)
        return {
            "email": email,
            "points": points,
            "rewardTier": "",
            "rewardTierName": "",
            "nextTier": "",
            "nextTierName": "", 
            "nextTierProgress": f'{progress}%',
        }

    for i in range(len(rewards)-1):
       if rewards[i]["points"] <= points < rewards[i+1]["points"]:
           return {
            "email": email,
            "points": rewards.points,
            "rewardTier": "",
            "rewardTierName": "",
            "nextTier": "",
            "nextTierName": "", 
            "nextTierProgress": f'{progress}%',
        }



def get_percent(customerPoints, tierPoints):
    return round((abs((100 + tierPoints) - customerPoints) / customerPoints) * 100.0, 2)
