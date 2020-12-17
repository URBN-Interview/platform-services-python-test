import json
import tornado.web
import tornado.escape

from pymongo import MongoClient
from bson.json_util import dumps
from tornado.gen import coroutine

import logging


class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        '''
        Returns customer's reward information
        Takes in:
          - email: string (User's email)

        '''
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        args = self.request.arguments
        try:
            email = tornado.escape.to_basestring(args["email"][0])
            customer = db.customers.find_one({"email": email})
            if customer:
                self.finish(dumps(customer))
            else:
                raise tornado.web.HTTPError(
                    status_code=404, log_message="Customer doesn't exist")
            return
        except KeyError as e:
            logging.debug(e)
            raise tornado.web.HTTPError(
                status_code=422, log_message="Email is required")

        raise tornado.web.HTTPError(
            status_code=400, log_message="Something went wrong")
