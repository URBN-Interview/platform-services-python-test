import json
import tornado.web

from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        try:
            request_body = json.loads(self.request.body.decode())
            self.write(request_body)
        except UnicodeError:
            self.set_status(400)
            self.write("Request body must be utf-8 encoded")
            self.finish()
        except json.decoder.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON")
            self.finish()