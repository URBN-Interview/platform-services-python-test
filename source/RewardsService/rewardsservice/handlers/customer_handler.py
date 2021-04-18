import json
import logging

import tornado.web
from tornado.web import MissingArgumentError

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        # set up logging
        logger = logging.getLogger()
        logger.info("/customer endpoint hit")

        # try to retrieve email query param, throw MissingArgumentError if unable to
        try:
            email_address = self.get_argument("emailAddress")

            # try to connect to DB, throw exception if unable to
            try:
                client = MongoClient("mongodb", 27017)
                db = client["Rewards"]
                customer_data = list(db.customers.find({"emailAddress": email_address}, {"_id": 0}))
                self.write(json.dumps(customer_data))

            except Exception as e:
                logger.error("Can't connect to server. Exception: %s", e)

        except MissingArgumentError as mae:
            logger.error("Query parameter missing. Exception: %s", mae)
