import tornado.web
import logging
import re

from pymongo import MongoClient
from typing import Union


class RewardsBaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]
        self.logger = logging.getLogger()

    def validate_email(self, email) -> Union[bool, str]:
        is_valid = re.compile(r"^\S+@\S+\.\S+$", flags=re.I)

        if not re.match(is_valid, email):
            return False, "Invalid email format"
        return True, None
