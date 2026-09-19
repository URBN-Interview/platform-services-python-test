import json
import re

import tornado.web

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        exc_info = kwargs.get("exc_info")
        message = "Internal server error"
        if exc_info and isinstance(exc_info[1], tornado.web.HTTPError):
            message = exc_info[1].log_message or self._reason
        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"error": message}))

    def get_json_body(self):
        try:
            return json.loads(self.request.body or b"{}")
        except (TypeError, ValueError):
            raise tornado.web.HTTPError(400, reason="Request body must be valid JSON")

    @staticmethod
    def validate_email(email):
        if not email or not isinstance(email, str) or not EMAIL_RE.match(email):
            raise tornado.web.HTTPError(400, reason="A valid 'email' is required")
        return email

    @staticmethod
    def validate_order_total(order_total):
        try:
            order_total = float(order_total)
        except (TypeError, ValueError):
            raise tornado.web.HTTPError(400, reason="'orderTotal' must be a number")
        if order_total <= 0:
            raise tornado.web.HTTPError(400, reason="'orderTotal' must be greater than 0")
        return order_total
