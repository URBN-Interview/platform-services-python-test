import json
import tornado.web
import pprint

from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerRequest(tornado.web.RequestHandler):
    @coroutine
    def get(self, email_id):

        return None
