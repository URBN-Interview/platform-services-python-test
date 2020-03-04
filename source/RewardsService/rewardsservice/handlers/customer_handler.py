import tornado.web
import json

from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import options

from util.validation import Validaton

class CustomerHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'
    error = None

    @coroutine
    def get(self):
        client = MongoClient(options.mongodb_host)
        db = client[self.collectionName]
        
        email = str(self.get_argument('email', ''))
        validateError = Validaton().emailValidation(email, 'email').validate()
        if validateError:
            self.error = validateError
            raise Exception(self.error.type)

        customers = list(db.customers.find({"email": email}, {"_id": 0}))
        self.write(json.dumps(customers))

    def write_error(self, status_code, **kwargs):
        if status_code == 500 and self.error:
            self.write({"type" : self.error.type, "context": self.error.context})
        elif status_code == 500:
            self.write({'message: Unknown Error'})