import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine



class CustomerHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
    	email_address = self.get_argument("email_address")
    	order_total = self.get_argument("order_total")
    	self.write({"email_address": email_address, "order_total": order_total})
