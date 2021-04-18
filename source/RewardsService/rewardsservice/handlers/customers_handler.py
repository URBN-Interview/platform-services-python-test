import json
import logging

import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        # set up logging
        logger = logging.getLogger()
        logger.info("/customers endpoint hit")

        # try to connect to DB, throw exception if unable to
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers_data = list(db.customers.find({}, {"_id": 0}))

            # check if any customers in DB, show error if not
            existing_customers = True if len(list(customers_data)) else False
            if existing_customers:
                self.write(json.dumps(customers_data))
            else:
                logger.error("No customer reward data exists in DB!")

        except Exception as e:
            logger.error("Can't connect to server. Exception: %s", e)
