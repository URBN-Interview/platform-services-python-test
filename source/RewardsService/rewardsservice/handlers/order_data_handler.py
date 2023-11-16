import json
import tornado.web
import math

from tornado.gen import coroutine
from .rewards_base import RewardsBaseHandler


class UserTierHandler(RewardsBaseHandler):
    """
    The UserTierHandler is for handling POST requests to the /rewards/order
    endpoint. It inherits the mongo client, db, and logger
    from RewardsBaseHandler.
    """

    @coroutine
    def post(self):
        """
        POST request expecting both a 'customerEmail' string and 'orderTotal' float
        in the body. Using this information, the handler validates the entered email
        and stores a mongo document with various reward tier information for
        the customer
        """

        customer_email = self.get_body_argument("customerEmail")
        customer_order_total = self.get_body_argument("orderTotal")
        points_clamp = lambda point, min_point, max_point: max(
            min(max_point, point), min_point
        )

        is_valid, err = self.validate_email(customer_email)
        if is_valid:
            user_query = {"email": customer_email}
            user_exists = self.db.users.find_one(user_query)
            if user_exists:
                total = points_clamp(
                    math.floor(user_exists["points"] + float(customer_order_total)),
                    0,
                    1000,
                )
            else:
                total = points_clamp(math.floor(float(customer_order_total)), 0, 1000)

            doc = yield self.util.hydrate_document(total, customer_email)
            self.db.users.update_one(user_query, {"$set": doc}, upsert=True)
            self.write(json.dumps(doc))

        else:
            self.logger.warn(err)

            raise tornado.web.HTTPError(400, reason=err)
