import json	
import tornado.web	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	

class CustomerHandler(tornado.web.RequestHandler):	
# GET Specific customer information	
    @coroutine	
    def get(self):	
        client = MongoClient(options.mongodb_host)	
        db = client["Customers"]	

        email = self.get_argument("email", "")	

        if email is not None:	
            customers = list(db.customers.find({"email": email}, {"_id": 0}))	
            self.write(json.dumps(customers))
        else:	
            print("email not found in database")	
