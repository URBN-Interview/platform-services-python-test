# Request handlers for the /customers resource: read back the rewards data
# that POST /orders calculates and stores in the customers collection.

import json

from tornado.web import HTTPError

from handlers.base_handler import BaseHandler


class CustomersHandler(BaseHandler):
    """Serves /customers.

    GET: returns the stored rewards data for every customer, sorted by email.
    Returns an empty list (not an error) when no customers exist yet.
    """

    async def get(self):
        customers = await (
            self.application.db.customers
            .find({}, {"_id": 0})          # {} = no filter (all customers), exclude _id
            .sort("emailAddress", 1)       # 1 = ascending, for a predictable order
            .to_list(None)                 # None = no limit
        )

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(customers))


class CustomerHandler(BaseHandler):
    """Serves /customers/{email}.

    GET: returns the stored rewards data for one customer, or 404 if that
    customer has never placed an order. The email is matched case-insensitively,
    the same way POST /orders stores it.
    """

    async def get(self, email):
        # Tornado passes the ([^/]+) part of the URL in, already URL-decoded (%40 -> @)
        email = email.strip().lower()
        if not email:
            raise HTTPError(400, reason="Email address is required")

        customer = await self.application.db.customers.find_one(
            {"emailAddress": email},
            {"_id": 0},     # exclude Mongo's _id - it isn't JSON serializable
        )
        if customer is None:
            raise HTTPError(404, reason="Customer not found")

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(customer))
