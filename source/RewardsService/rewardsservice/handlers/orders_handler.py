import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class OrdersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.write('<html><body><form action="/order" method="POST">'
                   '<label for="email">Email Address:</label>'
                   '<br>'
                   '<input type="text" name="email address">'
                   '<br>'
                   '<label for="order">Order Total:</label>'
                   '<br>'
                   '<input type="number" step="any" name="order total">'
                   '<br>'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Orders"]
        db.orders.remove()
        db.orders.insert({"email": self.get_body_argument("email address"), "cash": self.get_body_argument("order total")})
        orders = list(db.orders.find({}, {"_id": 0}))
        self.write(json.dumps(orders))
