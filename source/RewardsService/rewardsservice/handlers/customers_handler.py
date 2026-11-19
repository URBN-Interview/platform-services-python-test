"""
Request handler for multiple customers.

GET /customers
GET /customers/{customer_email}
POST /customers
"""
import json

from pymongo import MongoClient, errors
from .base_handler import BaseHandler

DB = BaseHandler.CLIENT["Rewards"]

class CustomersHandler(BaseHandler):

    async def get(self, email):
        """
        Get all the customers

        Supports endpoints: GET /customers, GET /customers/{customer_email}
        TODO: Add filtering, pagination, Support for single customer
        """
        # Send json of customers if they're in the db, otherwise empty 200 response
        try:
            if not email:
                customers = list(DB.customers.find({}, {"_id": 0}))
                self.write(json.dumps(customers, indent=4))
            else:
                # Implement email logic here, for now return first where email is email
                self.write({})
        except (errors.CollectionInvalid, TypeError):
            # Return an empty json response if nothing's been created yet
            self.write({})

    async def post(self):
        """
        Create a new customer.

        endpoint: POST /customers
        TODO: Add logic to create a new cuso
        """
        pass

