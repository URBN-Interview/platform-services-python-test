import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrdersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.write("Hello, kitty")

    @coroutine
    def post(self):
        orderEmailAddress = self.get_body_argument("email")
        orderAmount = self.get_body_argument("amount")
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + orderEmailAddress + " - " + orderAmount)
