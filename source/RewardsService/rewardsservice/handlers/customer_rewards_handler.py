import logging
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
from tornado import web
from helpers.validator import validator

class CustomerRewardsHandler(tornado.web.RequestHandler):
        
    @coroutine
    def get(self):  
        logging.getLogger().info('CustomerRewardsHandler.get()')     
        customer_rewards = list(self.rewards_db().customer_rewards.find({}, {"_id": 0}))
        self.write(tornado.escape.json_encode(customer_rewards))

    #post method for getting rewards based on email. Best Practice to not use PII in the get
    @coroutine
    def post(self): 
        logging.getLogger().info('CustomerRewardsHandler.post()')    
        customer_rewards = {}        
        data = json.loads(self.request.body)
        
        validateMessage = self.validateRequest(data)
        if (validateMessage['validate'] == 'Fail') :
            self.finish(validateMessage)  
            return

        emailAddress = data['email']
        print("Request: email {} ".format(emailAddress))
        customer_rewards = list(self.rewards_db().customer_rewards.find({ "email_address": { "$eq": emailAddress}}, {"_id": 0}))        
        self.write(tornado.escape.json_encode(customer_rewards))
    
    def validateRequest(self, data):
        response = {
                    "validate": "Pass",
                    "message":  ""
                } 
        if ('email' not in data.keys()):
            self.set_status(400)
            response['validate']= "Fail"
            response['message']= "Request doesn't have attribute 'email' present"                
            return response
        elif (data['email'] == ''):
            self.set_status(400)
            response['validate']= "Fail"
            response['message']= "Email Address is empty"            
            return response
        else: 
            if (validator.validateEmail(self, data['email']) is False): 
                self.set_status(400)
                response['validate']= "Fail"
                response['message']= "Email Address is invalid"                 
                return response

        return response    

    #get mongodb instance
    def rewards_db(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        return db   