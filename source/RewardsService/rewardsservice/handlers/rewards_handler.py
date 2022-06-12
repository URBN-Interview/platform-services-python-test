import json
import tornado.web

from tornado.gen import coroutine

class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        rewards = list(self.settings["db"].rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))
