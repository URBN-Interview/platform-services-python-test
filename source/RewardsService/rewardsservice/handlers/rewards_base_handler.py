import tornado.web
import logging
import re

from pymongo import MongoClient
from typing import Union
from utils.reward_utils import RewardTierUtil


class RewardsBaseHandler(tornado.web.RequestHandler):
    """
    RewardsBaseHandler is used for shared handler init vars
    as well as a shared email validation method.
    """

    def initialize(self):
        self.client = MongoClient("mongodb", 27017)
        self.db = self.client["Rewards"]
        self.logger = logging.getLogger()
        self.util = RewardTierUtil()

    def validate_email(self, email) -> Union[bool, str]:
        is_valid = re.compile(r"^\S+@\S+\.\S+$", flags=re.I)

        if not re.match(is_valid, email):
            return False, "Invalid email format"
        return True, None
