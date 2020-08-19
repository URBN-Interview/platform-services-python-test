import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


#following OOD design best practices, I am creating a class to handle the customers
class CustomerHandler(tornado.web.RequestHandler):

	# gets the email addrress and order total
    @coroutine
    def get(self):
    	# self.write("testing")
        client = MongoClient("mongodb", 27017)
    	# self.write(client.list_database_names())
        db = client["Customers"]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))
        # email_address = "test@test.com"
        email_address = self.get_argument("emailAddress")
        order_total = self.get_argument("orderTotal")
        # self.get_argument("emailAddress")
        email_exists = db.customers.find_one({'emailAddress': email_address}, {'_id': 0})
        # order_total = self.get_argument("orderTotal")
        #if customer does not already exist
        if not email_exists:
            #set rewardPoints to 0
            rewardPoints = 0
            self.write(json.dumps(list(db.customers.find({}, {"_id": 0}))))
    		#insert a new one to the database
            db.customers.insert({'emailAddress': email_address, 'rewardPoints': rewardPoints})
        else: 
          self.write(json.dumps(db.customers.find_one({"emailAddress": email_address}, {"_id": 0})))