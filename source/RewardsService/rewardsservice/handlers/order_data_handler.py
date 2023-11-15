import json
import logging

from tornado.gen import coroutine
from .rewards_base import RewardsBaseHandler


class OrderDataHandler(RewardsBaseHandler):
    def create_order_doc(self, email, total) -> dict:
        order_doc = {
            "customerEmail": email,
            "customerOrderTotal": float(total),
        }
        return order_doc

    @coroutine
    def post(self):
        customer_email = self.get_argument("customerEmail")
        customer_order_total = self.get_argument("orderTotal")

        try:
            is_valid = self.validate_email(customer_email)
            if is_valid:
                document = self.create_order_doc(customer_email, customer_order_total)
                self.write(json.dumps(document))

        except ValueError as e:
            logger = logging.getLogger()
            err = "Exception caught while validating email: {msg}".format(msg=e)
            logger.error(err)

            self.write_error(400, msg=err)
