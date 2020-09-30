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
        # email = "coco0@urbn.com"	
        email = self.get_argument("email", None)	
        if not email:	
            self.write("Email does not exist!")	
        else:	
            customers = list(db.customers.find({"email": email}, {"_id": 0}))	
            self.write(json.dumps(customers))	
