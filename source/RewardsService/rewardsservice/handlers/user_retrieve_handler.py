import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine


class UserRetrieveHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        user_email = self.get_body_argument("username")
        user_info = db.user_info.find_one(
            {"userEmail": user_email}, {"_id": 0})
        self.redirect("http://localhost:8000/rewards")
