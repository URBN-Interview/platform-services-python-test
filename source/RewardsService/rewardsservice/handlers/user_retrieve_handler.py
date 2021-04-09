import tornado.web
import re

from pymongo import MongoClient
from tornado.gen import coroutine


class UserRetrieveHandler(tornado.web.RequestHandler):

    def is_email(self, user_email):
        email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if (re.search(email_regex, user_email)):
            return True

    @coroutine
    def post(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        user_email = self.get_body_argument("username")
        if(self.is_email(user_email)):
            user_info = db.user_info.find_one({"userEmail": user_email}, {"_id": 0})
        self.redirect("http://localhost:8000/rewards")
