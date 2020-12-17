import json
import tornado.web

from pymongo import MongoClient
from bson.json_util import dumps
from tornado.gen import coroutine

import logging


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        '''
        Returns all customers' reward information
        '''
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        customers = db.customers.find({})
        self.finish(dumps(customers))
        return

        raise tornado.web.HTTPError(
            status_code=400, log_message="Something went wrong")
