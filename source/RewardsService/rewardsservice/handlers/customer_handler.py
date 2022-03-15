import json

import tornado
from mongo.mongo_manager import MongoManager
from tornado import web
from tornado.gen import coroutine
from util.validator import Validator
from util.server_error import UnknownError

from util.server_error import ServerError


class CustomerHandler(tornado.web.RequestHandler):
    error = None

    @coroutine
    def get(self, email):
        isValidEmail = Validator().emailValidation(email, 'email')
        if not isValidEmail:
            self.error = ServerError("InvalidRequestParams", "Invalid email address or email Address is missing in url")
            raise web.HTTPError(400)

        customerExist, isSuccess = MongoManager.getCustomerByEmail(email)

        if isSuccess:
            if customerExist:
                self.write(json.dumps(customerExist))
            else:
                self.error = ServerError("CustomerNotFound", "No customer found with the given email address")
                raise web.HTTPError(404)
        else:
            self.error = ServerError("ServiceUnavailable", "Please try again after some time")
            raise web.HTTPError(503)

    def write_error(self, status_code, **kwargs):
        if status_code in [400, 403, 404, 500, 503]:
            if not self.error:
                self.error = UnknownError()
            self.write({"type": self.error.type, "context": self.error.context, "error": self.error.error})
