import json

import tornado
from pymongo import MongoClient
from tornado import web
from tornado.gen import coroutine
from mongo.mongo_manager import MongoManager
from util.server_error import UnknownError
from util.server_error import ServerError


class CustomersHandler(tornado.web.RequestHandler):
    error = None
    @coroutine
    def get(self):
        customersExist, isSuccess = MongoManager.getCustomers()

        if isSuccess:
            if customersExist:
                self.write(json.dumps(customersExist))
            else:
                self.error = ServerError("NoCustomersPresentInDb", "No customers present in DB")
                raise web.HTTPError(404)
        else:
            self.error = ServerError("ServiceUnavailable", "Please try again after some time")
            raise web.HTTPError(503)

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
