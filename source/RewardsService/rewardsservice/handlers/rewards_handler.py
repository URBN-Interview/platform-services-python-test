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


class AddCustomerDatahandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        # Handle the POST request   

        def inner_wrapper(rewards_list,points):
            for reward in rewards_list:
                if reward['points']==points:
                    return reward
                
        # to calculate the rewards for an existing and new customer as well
        def calculate_rewards(customer_data):
            rewards = list(db.rewards.find({}, {"_id": 0}))
            points_list = [i.get('points') for i in rewards ]
            reward_points = customer_data.get('reward_points')
            if reward_points<points_list[0]:
                customer_data.update({
                    "next_reward_tier_progress":str(points_list[0]-customer_data.get('order'))+"%",
                })
            elif reward_points>=points_list[-1]:
                customer_data.update({
                    "reward_points" : points_list[-1],
                    "next_reward_tier":"The customer already reached to peak rewards",
                    "next_reward_tier_progress":"N/A",
                    "next_reward_name":"N/A"
                })
                return customer_data
            else:
                for i in range(0,len(points_list)-1):
                    if  points_list[i]<=int(reward_points)<=points_list[i+1]:
                        rewards_data = inner_wrapper(rewards,points_list[0])
                        reward_tier,reward_name = rewards_data.get('tier'),rewards_data.get('rewardName')
                        next_rewards_data = inner_wrapper(rewards,points_list[1])
                        next_reward_tier,next_reward_name = next_rewards_data.get('tier'),next_rewards_data.get('rewardName')
                        next_reward_tier_progress=str(points_list[i+1]-customer_data.get('order'))+"%"
                    customer_data.update(
                            {
                                "reward_tier":reward_tier,
                                "reward_name":reward_name,
                                "next_reward_tier":next_reward_tier,
                                "next_reward_name":next_reward_name,
                                "next_reward_tier_progress":next_reward_tier_progress
                     })
            return customer_data

        client = MongoClient("mongodb", 27017)
        db = client.get_database("Rewards")
        collection = db.get_collection("Customer")
        data = tornado.escape.json_decode(self.request.body)
        
        customer_data ={
            'customer_email':data.get('customer_email'),
            'order':data.get('order'),
            'reward_points' : round(data.get('order'))
        }

        data_exists = list(collection.find({"customer_email":customer_data.get('customer_email')}))
        if len(data_exists)>0:
            for existed_data in data_exists:
                customer_data.update({
                    'customer_email':data.get('customer_email'),
                    'order': customer_data.get('order') + int(existed_data.get('order')),
                    'reward_points': customer_data.get('reward_points') + int(existed_data.get('reward_points'))
                }
                )
            result = calculate_rewards(customer_data)
            collection.update_one({"customer_email" : customer_data.get('customer_email')},{"$set": result},upsert=True)
            self.write("Customer Data has been successful updated")
        else:
            result = calculate_rewards(customer_data)
            collection.insert_one(result)
            self.write("Customer Data has been successful registered")
        

class FetchAllCustomerDatahandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        # to fetch all the records in collection
        client = MongoClient("mongodb", 27017)
        db = client.get_database("Rewards")
        collection = db.get_collection("Customer")
        rewards = list(collection.find({}, {"_id": 0}))
        if rewards:
            self.write(json.dumps(rewards))
        else:
            self.write("No Customer Records Found")

    @coroutine
    def delete(self):
        # to delete the collection
        client = MongoClient("mongodb", 27017)
        db = client.get_database("Rewards")
        collection = db.get_collection("Customer")
        collection.drop()
        self.write("DELETE collection successful")

class FetchCustomerDatahandler(tornado.web.RequestHandler):

    @coroutine
    def get(self,slug):
        # to fetch one customer data from collection
        client = MongoClient("mongodb", 27017)
        db = client.get_database("Rewards")
        collection = db.get_collection("Customer")
        data_exists = list(collection.find({"customer_email":slug},{"_id": 0}))
        if data_exists:
            self.write(json.dumps(data_exists))
        else:
            self.write("No Customer Records Found")