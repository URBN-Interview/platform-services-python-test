import json
import tornado.web

from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        self.write("hello, world")

