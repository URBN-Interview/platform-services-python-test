import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class ProcessOrderHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        self.write("/processOrder")

