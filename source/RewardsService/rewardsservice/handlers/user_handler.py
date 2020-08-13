# this will be the user handler
import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UserHandler(tornado.web.RequestHandler):

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
        self.set_header("Content-Type", "application/json")  #text/plain
        self.write("Your email " + self.get_body_argument("email") + " your order total: " + self.get_body_argument("orderTotal") + "\n")
        
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {'_id': 0}))
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
            self.write("This email already exists")
            new_rewardPoints = old_customer['Reward Points'] + rewardPoints
            self.write(json.dumps(new_rewardPoints))
            db.Customers.update({'Email Address': email},{
                'Email Address': email,
                'Reward Points': new_rewardPoints})







# // deleting entries from the database.
        # myquery = { 'Email Address': "new@gmail.com"}
        # db.Customers.delete_one(myquery)

# #  Prints out all the customers in the table 
#         customer = list(db.Customers.find({}, {'_id': 0}))      #'Email Address': email
#         self.write(json.dumps(customer))
#         # self.write(json.dumps(rewards))
        test = db.Customers.find_one({'Email Address': email}, {'_id': 0})
        self.write(test)

   