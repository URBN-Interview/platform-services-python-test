import json
import tornado.web
import pprint

from pymongo import MongoClient 
from tornado.gen import coroutine

class CustomerOrder(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        #Assigning values received through the URL
        email = str(self.get_argument("email"))
        order = int(self.get_argument("order"))
        
        #Connecting to MongoDB service
        client = MongoClient("mongodb", 27017)
        db = client["Customers"]
        rewards_db = client["Rewards"]

        #Getting data from the server 
        cust_info = db.customers.find_one({"email": email})
        
        #Checking if the email is present in the database
        if cust_info!=None:
            cust_flag = True
            curr_points = cust_info["reward_points"]
            total_points  = order + curr_points
        else:
            cust_flag = False
            total_points = order 

        #Storing all the relevant info in a dictonary which will be later updated in the documents
        cust_dic = {}
        cust_dic["email"] = email
        cust_dic["reward_points"] = total_points

        #print(cust_dic)
        #lesser_vals = rewards_db.rewards.find({"points": {"$gte": total_points}}).distinct("points")
        #greater_vals = rewards_db.rewards.find({"points":{"$lte":total_points}}).distinct("points")
        
        #Calculting the value of the current and next tier 
        curr_tier_val = (total_points//100)*100
        next_tier_val = curr_tier_val + 100

        percentage_next_tier = (total_points % 100)/100

        #Special case - assigns N/A to values out of scope
        
        if curr_tier_val > 1000:
            cust_dic["reward_tier_name"] = "N/A"
            cust_dic["reward_tier"] = "N/A"
            cust_dic["next_reward_tier_name"] = "N/A"
            cust_dic["next_reward_tier"] = "N/A"
            cust_dic["next_reward_tier_progress"] = "N/A"
        else:
            if curr_tier_val < 100:
                cust_dic["reward_tier_name"] = "N/A"
                cust_dic["reward_tier"] = "N/A"
            else:
                #Connecting with the Rewards database and getting all the data associated reward points
                current_tier_dic = rewards_db.rewards.find_one({"points": curr_tier_val})
                cust_dic["reward_tier"] = current_tier_dic["tier"]
                cust_dic["reward_tier_name"] = current_tier_dic["rewardName"]

            next_tier_dic = rewards_db.rewards.find_one({"points":next_tier_val})
            cust_dic["next_reward_tier_name"] = next_tier_dic["rewardName"]
            cust_dic["next_reward_tier"] = next_tier_dic["tier"]
            cust_dic["next_reward_tier_progress"] = str(percentage_next_tier)

        #Update the collection on the database
        if cust_flag is False:
            db.customers.insert(cust_dic)
            print("Email added successfully - ", email)
        else:
            db.customers.update({"email":email},cust_dic)
            print("Update successful")

