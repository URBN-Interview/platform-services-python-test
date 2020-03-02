import tornado.web


from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    collectionName = 'Customers'

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client[self.collectionName]
        validation = Validaton()

        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))

        validation.emailValidation(email).currencyValidation(orderTotal).validate()
        customer = db.customers.insert({"email": email, "orderTotal": orderTotal})

        self.write({"email": email, "orderTotal": orderTotal})


