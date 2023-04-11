import pymongo
import json

from pymongo.errors import PyMongoError
from tornado.web import RequestHandler, HTTPError

client = pymongo.MongoClient("mongodb", 27017)
customer_db = client["CustomerData"]


class RewardsDataHandler(RequestHandler):
    """
    To fetch data from mongodb for single customer
    """
    def get(self):
        try:
            email = self.get_argument('email')
            customer_data = customer_db.customerdata.find_one({'email': email})

            if customer_data is None:
                self.set_status(404)
                self.write({'error': 'No rewards data found for email: {}'.format(email)})
            else:
                rewards_json = json.dumps(customer_data, default=str)
                self.set_header('Content-Type', 'application/json')
                self.write(rewards_json)
        except ValueError:
            raise HTTPError(400, "Invalid order total")

        except PyMongoError:
            raise HTTPError(500, "Error storing rewards data")
