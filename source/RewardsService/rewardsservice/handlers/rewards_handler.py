import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine
import utils
import mongo_utils
from responses import JsonResponse
from bson.json_util import dumps, loads


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        db = mongo_utils.get_mongo_connection()
        rewards = list(db.rewards.find({}, {"_id": 0}))
        result = JsonResponse(code=200, status="SUCCESS", message="Rewards Categories Generated", extra_fields=rewards)
        result.response(self)


class CustomerRewards(tornado.web.RequestHandler):

    @coroutine
    def get(self, slug=None):
        db = mongo_utils.get_mongo_connection()
        if slug:
            customer = mongo_utils.get_customers_data(db, slug)
            customers = [customer] if customer else []
        else:
            customers = mongo_utils.get_customers(db)
        result = JsonResponse(code=200, status="SUCCESS", message="Success", extra_fields=customers)
        result.response(self)

    @coroutine
    def post(self, slug=None):
        input_data = json.loads(self.request.body)
        errors = utils.validate_customer_data(input_data)
        if errors:
            result = JsonResponse(code=400, status="FAIL", message="Input Data has errors, Please Check", errors=errors)
            result.response(self)
            return
        email = input_data.get("email")
        db = mongo_utils.get_mongo_connection()
        customer = mongo_utils.create_customer(db, input_data)
        if customer.get("_id"):
            del customer["_id"]
        result = JsonResponse(code=200, status="SUCCESS", message="Successfully Customer Update", extra_fields=[customer])
        result.response(self)

