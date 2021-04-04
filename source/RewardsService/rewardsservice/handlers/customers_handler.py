import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customersList = list(db.customers.find({},{"_id": 0}))
            
            self.write(json.dumps(customersList))

        except Exception as e:
            self.write(json.dumps({'status':'error','error':str(e)}))
