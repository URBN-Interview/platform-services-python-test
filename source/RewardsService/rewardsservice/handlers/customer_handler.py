import json

import tornado
from mongo.mongo_manager import MongoManager
from tornado.gen import coroutine
from util.validator import Validator
from util.server_error import UnknownError


class CustomerHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'
    error = None

    @coroutine
    def get(self):
        email = str(self.get_argument('email', ''))

        validateError = Validator().emailValidation(email, 'email').validate()
        if validateError:
            self.error = validateError
            raise Exception(self.error.type)

        client = MongoManager().client
        db = client[self.collectionName]
        customers = list(db.customers.find({"email": email}, {"_id": 0}))
        if customers is None:
            self.set_status(404)
        self.write(json.dumps(customers))

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
