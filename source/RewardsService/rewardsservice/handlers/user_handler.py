# this will be the user handler
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UserHandler(tornado.web.RequestHandler):

    def getTier(self, points):
        if points >= 900: return "J"
        elif points >= 800: return "I"
        elif points >= 700: return "H"
        elif points >= 600: return "G"
        elif points >= 500: return "F"
        elif points >= 400: return "E"
        elif points >= 300: return "D"
        elif points >= 200: return "C"
        elif points >= 100: return "B"
        elif points >= 0: return "A"
        else : return "J"

    def getNextTier(self, myTier):
        nextTier = chr(ord(myTier) + 1)
        if nextTier > 'J':
            nextTier = 'J'
        return nextTier

        

    @coroutine
    def get(self):
        # handles errors for foregin email and orderTotal input 
        self.write('<html><body><form action="/user" method="POST">'
        '<label for="email">Enter your email:</label>'
            '<input type="email" name="email"><br>'
        '<label for="orderTotal">Enter your Order Total:</label>'
            '<input type="number" min="0.01" step="0.01" name="orderTotal"><br>'
            '<input type="submit" value="Submit">'
            '</form></body></html>')


    def post(self):
        self.set_header("Content-Type", "application/json")
        self.write("Your email " + self.get_body_argument("email") + " your order total: " + self.get_body_argument("orderTotal") + "\n")
        
        client = MongoClient("mongodb", 27017)
        rewards_db = client["Rewards"]
        rewards = list(rewards_db.rewards.find({"tier": "A"}, {"_id": 0}))
        self.write(json.dumps(rewards))
        db = client['Customers']
        email = self.get_body_argument('email', None)
        orderTotal = self.get_body_argument('orderTotal', float)

        convert_to_float = float(orderTotal)
        # check for whole number 
        if (convert_to_float % 1 != 0):
            rewardPoints = convert_to_float // 1
        else:
            rewardPoints = convert_to_float 

    # Check for a new email 
        old_customer = db.Customers.find_one({'Email Address': email}, {'_id': 0})
        new_rewardPoints = 0
        if not old_customer:
            # insert new customers into the data base
            db.Customers.insert(
            {'Email Address': email, 'Reward Points': rewardPoints}
            )
            
        else:
            self.write("This customer already exists  ")
            new_rewardPoints = old_customer['Reward Points'] + rewardPoints 
            self.write(json.dumps(new_rewardPoints) + "\n")
            current_tier = self.getTier(new_rewardPoints)
            nextTier = self.getNextTier(current_tier)
  
            reward_tier_name = rewards_db.rewards.find_one({'tier': current_tier}, {'_id': 0})['rewardName']
            next_reward_tier_name = rewards_db.rewards.find_one({'tier': nextTier}, {'_id': 0})['rewardName']
 
            db.Customers.update({'Email Address': email},{
                'Email Address': email,
                'Reward Points': new_rewardPoints,
                'Reward Tier': current_tier,
                'Reward Tier Name': reward_tier_name,
                'Next Reward Tier': nextTier,
                'Next Reward Tier Name': next_reward_tier_name})


#### // deleting entries from the database.
        # myquery = { 'Email Address': "new@gmail.com"}
        # db.Customers.delete_one(myquery)

# #  Prints out all the customers in the table 
        # customer = list(db.Customers.find({}, {'_id': 0}))      #'Email Address': email
        # self.write(json.dumps(customer)+ "\n")
#         # self.write(json.dumps(rewards))
        test = db.Customers.find_one({'Email Address': email}, {'_id': 0})
        self.write(test)

   