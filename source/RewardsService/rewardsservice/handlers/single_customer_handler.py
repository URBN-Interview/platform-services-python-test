import tornado.web

from pymongo import MongoClient


class SingleCustomerHandler(tornado.web.RequestHandler):

    email = None

    def post(self):
        """Get customers email address from field entry"""
        try:
            SingleCustomerHandler.email = self.get_arguement("email address")
        except:
            print("Error getting email address")

    def get(self):
        """Search for customers info in database and return it"""
        try:
            client = MongoClient("mongodb", 27017)
            db = client["Rewards"]
            customers = list(db.customers.find({}, {"_id": 0}))

            for x in customers:
                for key, value in x.iteritems():
                    if key == 'email' and value == SingleCustomerHandler.email:
                        customer_info = x
                        return customer_info

        except:
            print("Error finding customer info")
