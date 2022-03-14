import json

import tornado
from pymongo import MongoClient
from tornado.gen import coroutine
from mongo.mongo_manager import MongoManager
from util.server_error import UnknownError


class CustomersHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'

    @coroutine
    def get(self):
        email = str(self.get_argument('email', ''))
        client = MongoManager().client
        db = client[self.collectionName]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
