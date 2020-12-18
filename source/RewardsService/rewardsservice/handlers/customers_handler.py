import json
import tornado.web

from tornado.gen import coroutine


class CustomersHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    # Endpoints 2 and 3
    @coroutine
    def get(self):
        emails = self.get_arguments("email_address")
        if len(emails) == 0:
            all_customers = self.db.get_all_customers()
            self.write(json.dumps(all_customers))
            return

        customer = self.db.get_customer_by_email_address(emails[0])
        self.write(json.dumps(customer))

    # Endpoint 1
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

        email_address, error = self.validate_email_address(request_body)
        if error is not None:
            self.set_status(error.get("status_code"))
            self.write(error.get("message"))
            return

        order_total, error = self.validate_order_total(request_body)
        if error is not None:
            self.set_status(error.get("status_code"))
            self.write(error.get("message"))
            return

        upserted_customer = self.db.upsert_customer(email_address, order_total)
        self.write(json.dumps(upserted_customer))


    def validate_email_address(self, request_body):
        if "email_address" not in request_body:
            return None, {
                "message": self.missing_field_error_message("email_address"),
                "status_code": 400
            }

        # TODO: add validation here if not performed on client side
        return request_body["email_address"], None


    def validate_order_total(self, request_body):
        if "order_total" not in request_body:
            return None, {
                "message": self.missing_field_error_message("order_total"),
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


    def missing_field_error_message(self, missing_field):
        return "Missing required field '{}'".format(missing_field)