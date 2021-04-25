import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

class Endpoint3(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        # if 'users' in db.list_collection_names():
        #     pass
        # else:
        #     db.create_collection('users')
        
        # db.users.remove()
        # mycol = db["Users"]
        # db.users.insert({
        #     "email": 'test@email.com', 
        #     "rewardPoints": 150, 
        #     "rewardTier": 'A',
        #     "rewardTierName": "5% off purchase",
        #     "nextRewardTier": "B",
        #     "nextRewardTierName": "10% off purchase",
        #     "nextRewardTierProgress": "75%"
        # })
        users = list(db.users.find({}, {"_id": 0}))

        self.write(json.dumps(users))

    # def get(self):
    #     client = MongoClient("mongodb", 27017)
    #     db = client["Rewards"]
    #     rewards = list(db.rewards.find({}, {"_id": 0}))
    #     users = list(db.users.find({}, {"_id": 0}))
    #     reward_points = 250
    #     email = "test@email.com"
    #     for reward in rewards:
    #         if reward['points'] > reward_points:
    #             # break
                
    #             reward_index = rewards.index(reward)
    #             # print(reward_index)
    #             # rewards_list = list(enumerate(reward_index))
    #             # first_reward = rewards_list.pop(0)
    #             # reward_index_list = [reward_index]
    #             # for index in reward_index:
    #             #     reward_index_list.append(index)
    #             # reward_index_low = min(reward_index_list)
    #             # res = list(filter(lambda i: rewards.index(i) != reward_index, rewards))
    #             # rewards.pop(reward_index)
    #             # res = [i for i in rewards if not (rewards.index(i) == reward_index)]
    #             # res.pop()

    #             self.write(json.dumps(reward['rewardName']))
    #             reward_index -= 1
    #             # self.write(json.dumps(reward_index))
    #             break
                
                


    #     for user in users:
    #         if user['email'] == email:

    #             # user_index = user.index(user)
    #             users.pop(user)
    #             # return self.write(json.dumps(user))

    #             self.write(json.dumps(user))
    #         else:
    #             return self.write("there's no user with this email")

    #     # give results an index, then return the first one