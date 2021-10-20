import json
import logging

from bson.json_util import dumps
from tornado.gen import coroutine

from .root_handler import MongoMixin

log = logging.getLogger(__name__)


class RewardTiersHandler(MongoMixin):

    @coroutine
    def get(self):
        log.info('Getting reward tiers')
        tiers = self.db.rewards.find({})  # return all
        response = []
        for tier in tiers:
            if tier.get('email'):  # document is a user, skip
                continue
            response.append(self.response_serializer(tier))
        self.write({'tiers': response})

    @staticmethod
    def response_serializer(tier):
        return json.loads(dumps(tier, sort_keys=True))
