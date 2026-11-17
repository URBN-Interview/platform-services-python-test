from urllib.parse import unquote

import tornado.web

from handlers.base_handler import BaseHandler
from rewards_calculator import ValidationError, normalize_email


class CustomersHandler(BaseHandler):
    """GET /customers - rewards data for all customers (Endpoint 3)."""

    async def get(self):
        self.write_json(await self.repository.get_customers())


class CustomerHandler(BaseHandler):
    """GET /customers/{email} - rewards data for one customer (Endpoint 2)."""

    async def get(self, email):
        try:
            email = normalize_email(unquote(email))
        except ValidationError as e:
            raise tornado.web.HTTPError(400, reason=str(e))

        customer = await self.repository.get_customer(email)
        if customer is None:
            raise tornado.web.HTTPError(404, reason="Customer '{}' not found".format(email))
        self.write_json(customer)
