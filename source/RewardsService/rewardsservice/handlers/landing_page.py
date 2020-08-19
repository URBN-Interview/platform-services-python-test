import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class LandingPage(tornado.web.RequestHandler):

    @coroutine
    def get(self):
    	client = MongoClient("mongodb", 27017)
    	self.write("Landing Page")