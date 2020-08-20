import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


#following OOD design best practices, I am creating a class to handle the customer operations and rewards
class CustomerHandler(tornado.web.RequestHandler):
    client = MongoClient("mongodb", 27017)

    @coroutine
    def get(self):
        # self.write(client.list_database_names()) 
        db = self.client["Customers"]
        email_address = self.get_argument("emailAddress", None)
        self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))
        # if not email_exists:
        #     self.write("This email doesn't exist in the system!")
        #     #insert a new one to the database
        # else: 
        #   self.write(db.customers.find_one({"emailAddress": email_address}, {"_id": 0}))



    # gets the email addrress and order total
    @coroutine
    def post(self):
    	# self.write("testing")
    	# self.write(client.list_database_names())
        # self.write(json.dumps(customers))
        # email_address = "test@test.com"
        db = self.client["Customers"]
        email_address = self.get_argument("emailAddress", None)
        order_total = self.get_argument("orderTotal", None)
        # remove decimals
        order_total_trun = trun(order_total)
        # self.get_argument("emailAddress")
        email_exists = db.customers.find_one({"emailAddress": email_address}, {"_id": 0})
        # order_total = self.get_argument("orderTotal")
        #customers earn 1 point for each dollar they spend
        rewardPoints = order_total_trun
        #if customer does not already exist
        if not email_exists:
            # self.write(json.dumps(list(db.customers.find({}, {"_id": 0}))))
    		#insert a new one to the database
            db.customers.insert({"emailAddress": email_address, "rewardPoints": rewardPoints})
        else:
            db.customers.update_one({"emailAddress" : email_address},{ "$set": {"rewardPoints" : customers["rewardPoints"] + rewardPoints}}) 
            self.write(json.dumps(db.customers.find_one({"emailAddress": email_address}, {"_id": 0})))

    # def get_rewards(self, email_address):

    # def set_rewards(self):








