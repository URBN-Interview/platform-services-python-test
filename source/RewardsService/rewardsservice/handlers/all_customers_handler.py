import tornado.web
import json

from util.server_error import UnknownError
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

class AllCustomersHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'

    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        customers = list(db.customers.find({}, {"_id": 0}))
        self.write(json.dumps(customers))

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type" : self.error.type, "context": self.error.context, "error": self.error.error})