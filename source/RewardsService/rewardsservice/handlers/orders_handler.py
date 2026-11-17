import tornado.web

from handlers.base_handler import BaseHandler
from rewards_calculator import ValidationError, normalize_email, parse_order_total


class OrdersHandler(BaseHandler):
    """POST /orders - record a customer's order and update their rewards (Endpoint 1).

    Request body: {"email": "customer01@gmail.com", "orderTotal": 100.80}
    Responds 201 with the customer's updated rewards data.
    """

    async def post(self):
        body = self.read_json_body()
        missing = [field for field in ("email", "orderTotal") if field not in body]
        if missing:
            raise tornado.web.HTTPError(400, reason="Missing required field(s): {}".format(", ".join(missing)))

        try:
            email = normalize_email(body["email"])
            order_total = parse_order_total(body["orderTotal"])
        except ValidationError as e:
            raise tornado.web.HTTPError(400, reason=str(e))

        rewards = await self.repository.add_order(email, order_total)
        self.set_header("Location", "/customers/{}".format(email))
        self.write_json(rewards, status=201)
