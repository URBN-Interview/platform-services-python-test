import tornado.web
import re

from pymongo import MongoClient


class RewardsBaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]

    def write_error(self, status_code, msg="base error value", **kwargs):
        if status_code in [400, 404, 403, 406]:
            self.set_status(status_code)
            self.write("Error: {code}\n{msg}".format(code=status_code, msg=msg))
        else:
            self.write("Unexpected Error: {}".format(status_code))

    def validate_email(self, email) -> bool:
        is_valid = re.compile(r"^\S+@\S+\.\S+$", flags=re.I)

        if not is_valid.match(email):
            raise ValueError("Invalid email format")
        return True
