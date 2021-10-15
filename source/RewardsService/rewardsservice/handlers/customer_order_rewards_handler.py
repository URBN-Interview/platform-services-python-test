import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerOrderRewardsHandler(tornado.web.RequestHandler):
    
    @coroutine
    def post(self): 
        try:                                              
            data = json.loads(self.request.body)
            emailAddress = data['email']
            orderTotal = int(float(str(data['order_total']))      )   
            print("Request: email {} and order_total: {} ".format(emailAddress, orderTotal))                                            

            #find if the customer_rewards collection exist        
            #find if the customer_reward exist based on email_address
            customer_reward = self.customer_reward(emailAddress)            
            #if it does exist then update
            if (customer_reward) is not None:                
                customer_reward["reward_points"] += orderTotal            
                customer_reward = self.update_customer_reward(customer_reward, customer_reward["reward_points"])            
                record_updated = self.rewards_db().customer_rewards.update_one({"email_address": emailAddress}, {"$set": customer_reward})
                print("number of records updated  : {}".format(record_updated))                
            else:   
                #if cusomter_reward doesn't exist then insert
                customer_reward = {}
                customer_reward["email_address"] = emailAddress
                customer_reward["reward_points"] = orderTotal
                customer_reward = self.update_customer_reward(customer_reward, orderTotal)                                                            
                record_inserted = self.rewards_db().customer_rewards.insert_one(customer_reward)
                print("number of records inserted: {}".format(record_inserted))                
        
        except Exception as ex:
            print (ex)

        self.write(json.dumps({"Message":"Success"}))
    
    
    #customer_reward will return the row for the provided email address or None   
    def customer_reward(self, email_address):
        customer_reward = self.rewards_db().customer_rewards.find_one({'email_address': email_address})   
        return customer_reward
    
    #get mongodb instance
    def rewards_db(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        return db  
    
    #method to calculate the next tier progress
    def get_next_reward_tier_progress(self, reward_tiers, reward_points): 
        print("           get_next_reward_tier_progres                 ")
        curr_reward_tier = reward_tiers['curr_reward_tier']
        next_reward_tier = reward_tiers['next_reward_tier']           
        if (curr_reward_tier["tier"] == next_reward_tier["tier"]):
            return 0.0
        else:      
            progress = ((int(next_reward_tier['points']) - reward_points) / int(next_reward_tier['points']) ) * 100  
            progress = "%.2f" % round(progress, 1)                
            return progress

    #update the customer_reward with common attributes between insert and udpate operations
    def update_customer_reward(self, customer_reward, reward_points):         
        reward_tiers = self.get_curr_next_tier(reward_points)
        curr_reward_tier = reward_tiers['curr_reward_tier']
        next_reward_tier = reward_tiers['next_reward_tier']        
        customer_reward["reward_tier"] = curr_reward_tier["tier"]
        customer_reward["reward_tier_name"] = curr_reward_tier["rewardName"]
        customer_reward["reward_points"] = reward_points
        customer_reward["next_reward_tier"] = next_reward_tier["tier"]
        customer_reward["next_reward_tier_name"] = next_reward_tier["rewardName"]        
        customer_reward["next_reward_tier_progress"] = self.get_next_reward_tier_progress(reward_tiers, reward_points)
        print(customer_reward)
        return customer_reward 

    #implement better search algo to find the right range
    #
    def get_curr_next_tier(self, total_points):
        print("              get_curr_next_tier()            ")         
        rewards = list(self.rewards_db().rewards.find().sort("points", +1))
        reward_tiers = {}
        if rewards: 
            prev_reward_tier = None   
            curr_reward_tier = None       
            for i in range(0, len(rewards)):
                curr_reward_tier = rewards[i]                
                if (prev_reward_tier) is None:
                    if (curr_reward_tier['points'] > total_points):
                        reward_tiers['next_reward_tier'] = curr_reward_tier                
                        reward_tiers['curr_reward_tier'] = { "tier":"", "rewardName":"" }
                        return reward_tiers
                elif (curr_reward_tier['points'] > total_points and prev_reward_tier['points'] <= total_points):                    
                    reward_tiers['next_reward_tier'] = curr_reward_tier
                    reward_tiers['curr_reward_tier'] = prev_reward_tier
                    return reward_tiers
                prev_reward_tier = curr_reward_tier
                
            #if the current reward doesn't match with any of the combinations then it's above the last reward tier
            reward_tiers['curr_reward_tier'] = curr_reward_tier
            reward_tiers['next_reward_tier'] = curr_reward_tier       
        return reward_tiers
            
