import tornado.web
import json
import time

from pymongo import MongoClient

email = None


class SingleCustomerHandler(tornado.web.RequestHandler):
    """Gets customer email from form and returns their rewards info"""

    def post(self):
        """Get customers email address from field entry"""
        try:
            global email

            email = self.get_argument('search_email')

            self.get()
        except ValueError:
            self.write("A value error occurred")
        except TypeError:
            self.write("A type error has occurred")
        except RuntimeError:
            print("Error getting email address")

    def get(self):
        """Search for customers info in database and return it"""
        try:
            global email
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]

            customer_info = db.customers.find_one({"email": email}, {"_id": 0})
            self.write(json.dumps(customer_info))
            return
        except KeyError:
            self.write("A key error occurred")
        except ValueError:
            self.write("A value error occurred")
        except TypeError:
            self.write("A type error has occurred")
        except RuntimeError:
            print("Error finding customer info")
