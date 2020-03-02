import tornado.web


from util.validation import Validaton
from pymongo import MongoClient
from tornado.gen import coroutine


class CustomerHandler(tornado.web.RequestHandler):
    

    @coroutine
    def post(self):
        email = str(self.get_argument('email', ''))
        orderTotal = str(self.get_argument('orderTotal', ''))
        
        Validaton().emailValidation(email).currencyValidation(orderTotal).validate()
        self.write({"email": email, "orderTotal": orderTotal})


