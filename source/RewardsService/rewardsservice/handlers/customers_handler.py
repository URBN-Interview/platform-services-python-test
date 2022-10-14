import tornado.web
from tornado.gen import coroutine
import json


class CustomersHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    # Endpoint 3- all customers reward information
    @coroutine
    def get(self):
        all_customers = self.db.get_every_customers()
        self.write(json.dumps(all_customers))

    # Endpoint 1- takes email address of the customer and order total, calculates reward points.
    # Returns data on Reward Points, Reward Tier, Reward Tier Name, Next Reward Tier, Next Reward Tier Name, Next Reward Tier Progress
    @coroutine
    def post(self):
        try:
            request_body = json.loads(self.request.body.decode())
        except UnicodeError:
            self.set_status(400)
            self.write("Request body must be utf-8 encoded")
            return
        except json.decoder.JSONDecodeError:
            self.set_status(400)
            self.write("Invalid JSON")
            return

        email_address, error = self.email_address_validation(request_body)
        if error is not None:
            self.set_status(error.get("status_code"))
            self.write(error.get("message"))
            return

        order_total, error = self.total_order_validation(request_body)
        if error is not None:
            self.set_status(error.get("status_code"))
            self.write(error.get("message"))
            return

        customer_asserted = self.db.customer_assertion(email_address, order_total)
        self.write(json.dumps(customer_asserted))


    def email_address_validation(self, request_body):
        if "email_address" not in request_body:
            return None, {
                "message": self.error_message_missing_field("email_address"),
                "status_code": 400
            }

        return request_body["email_address"], None


    def total_order_validation(self, request_body):
        if "order_total" not in request_body:
            return None, {
                "message": self.error_message_missing_field("order_total"),
                "status_code": 400
            }

        try:
            order_total = float(request_body["order_total"])
        except ValueError:
            return None, {
                "message": "'order_total' must be a number",
                "status_code": 400
            }

        if round(order_total, 2) != order_total:
            return None, {
                "message": "'order_total' must be a number with no more than two values after the decimal point",
                "status_code": 400
            }

        return order_total, None


    def error_message_missing_field(self, missing_field):
        return "Missing required field '{}'".format(missing_field)