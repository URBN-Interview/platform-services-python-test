import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class IndexHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        self.write("Try /rewards, /processOrder, /customer, or /customers")
