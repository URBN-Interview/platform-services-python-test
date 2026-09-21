import json
import re

import tornado.web

from handlers.base_handler import BaseHandler


class CustomersHandler(BaseHandler):

    async def get(self):
        query = {}
        email_filter = self.get_query_argument("email", default=None)
        if email_filter:
            query["email"] = {"$regex": re.escape(email_filter), "$options": "i"}

        customers = await self.application.db.customerRewards.find(
            query, {"_id": 0}
        ).to_list(length=None)
        self.write(json.dumps(customers))


class CustomerHandler(BaseHandler):

    async def get(self, email):
        customer = await self.application.db.customerRewards.find_one(
            {"email": email}, {"_id": 0}
        )
        if customer is None:
            raise tornado.web.HTTPError(
                404, reason="No rewards data found for email '{}'".format(email)
            )
        self.write(json.dumps(customer))
