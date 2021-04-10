import json
import tornado.web
import math

from pymongo import MongoClient
from tornado.gen import coroutine
from rewardsservice.utils.utils import calculateTotalPoints, updateCustomerPoints, calculateCurrentRewardTierName,calculateCurrentPointsTier,calculateNextPointsTier,calculateNextRewardTierName,calculateNextRewardTierProgress,composeCustomerData

class CustomerRewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        #checks for what params are available
        email = self.get_argument('email', None)
        orderTotal = self.get_argument('ordertotal', None)
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"] 

        #Checks if there are any params, if not returns all customer data
        if((email == None or email == "") and (orderTotal == None or orderTotal == "")):
            customerList = list(db.customers.find())
            payload = []
            for customer in range(len(customerList)):
                # totalpoints is the total amount of points for a particular customer
                totalpoints = customerList[customer]['rewardpoints']
                customerData = composeCustomerData(
                    customerList[customer]["email"],
                    totalpoints,
                    calculateCurrentRewardTierName(db,totalpoints),
                    calculateCurrentPointsTier(db,totalpoints),
                    calculateNextPointsTier(db,totalpoints),
                    calculateNextRewardTierName(db,totalpoints),
                    calculateNextRewardTierProgress(db,totalpoints)
                )
                payload.append(customerData)
            self.write(json.dumps(payload, sort_keys=False))

        else:
            # Adds the new points to the customer data and updates the entry to reflect the 
            # new total
            totalpoints = calculateTotalPoints(db, orderTotal, email)
            updateCustomerPoints(db, email, totalpoints)
            customer = list(db.customers.find({"email":email}, {"_id": 0}))
            payload = composeCustomerData(
                customer[0]["email"],
                totalpoints,
                calculateCurrentRewardTierName(db,totalpoints),
                calculateCurrentPointsTier(db,totalpoints),
                calculateNextPointsTier(db,totalpoints),
                calculateNextRewardTierName(db,totalpoints),
                calculateNextRewardTierProgress(db,totalpoints)
            )
            self.write(json.dumps(payload))

        