import json
import tornado.web
from tornado import escape
from pymongo import MongoClient
from tornado.gen import coroutine
from helpers.validator import validator

class CustomerOrderRewardsHandler(tornado.web.RequestHandler):
    
    @coroutine
    def post(self): 
        try:                                              
            request_data = escape.json_decode(self.request.body)
            emailAddress = request_data['email']
            orderTotal = int(float(str(request_data['order_total'])))   
            print("Request: email {} and order_total: {} ".format(emailAddress, orderTotal))                                            
            
            validateMessage = self.validateRequest(request_data)
            if (validateMessage['validate'] == 'Fail') :
                self.finish(validateMessage)  
                return
        
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
            
            self.set_status(200)       
        except Exception as ex:
            print (ex)

        self.write(json.dumps({"Message":"Success"}))
    
    #validate all request parameter which are required
    def validateRequest(self, data):
        response = {
                    "validate": "Pass",
                    "message":  ""
                } 
        if (data['email'] == ''):
            self.set_status(400)            
            response['validate']= "Fail"
            response['message']= "Email Address is empty"                
            return response
        else: 
            if (validator.validateEmail(self, data['email']) is False): 
                self.set_status(400)            
                response['validate']= "Fail"
                response['message']= "Email Address is invalid."                
                return response
        return response   
    
    
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

    #implemented better algorithm to find the range in O(logn) time
    def get_curr_next_tier(self, total_points):
        print("              get_curr_next_tier()            ")         
        rewards = list(self.rewards_db().rewards.find().sort("points", +1))
        reward_tiers = {}
        if rewards: 
            Left = 0
            Right = (len(rewards))

            if total_points < rewards[0]['points']:
                reward_tiers['next_reward_tier'] = rewards[0]                
                reward_tiers['curr_reward_tier'] = { "tier":"", "rewardName":"" }
            elif total_points > rewards[Right-1]['points']:
                print("current_tier: " , ['points']) 
                print("next_tier: " , rewards[Right-1]['points'])
                reward_tiers['curr_reward_tier'] = rewards[Right-1]
                reward_tiers['next_reward_tier'] = rewards[Right-1] 
            else: 
                while ((Left+1)<Right):
                    mid = int((Left+Right)/2)                    
                    if rewards[mid]['points'] > total_points:
                        Right = mid
                    else:
                        Left = mid
                reward_tiers['curr_reward_tier'] = rewards[Left]['points']
                reward_tiers['next_reward_tier'] = rewards[Right]['points']
                   
        return reward_tiers        
