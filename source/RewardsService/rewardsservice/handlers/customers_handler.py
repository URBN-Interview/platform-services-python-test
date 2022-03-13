import tornado
from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        self.write("success")