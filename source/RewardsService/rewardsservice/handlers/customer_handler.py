import json
import tornado.web

from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    # Endpoint 2
    @coroutine
    def get(self):
        email = self.get_argument("email_address")
        if not email:
            self.set_status(400)
            self.write("Missing `email_address` query parameter")
            return

        customer = self.db.get_customer_by_email_address(email)
        self.write(json.dumps(customer))