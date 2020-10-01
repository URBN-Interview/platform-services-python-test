import json	
import tornado.web	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	
	
class AllCustomerHandler(tornado.web.RequestHandler):	

    @coroutine	
    def get(self):	
        client = MongoClient(options.mongodb_host)	
        db = client["Customers"]	
        customers = list(db.customers.find({}, {"_id": 0}))	
        self.write(json.dumps(customers))	
