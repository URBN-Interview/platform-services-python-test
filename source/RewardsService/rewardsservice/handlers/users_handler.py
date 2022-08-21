import json
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from settings import JSON_MIME_TYPES

class UsersHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.database = MongoClient("mongodb", 27017)["Rewards"]

    @coroutine
    def prepare(self):
        if self.request.headers["Content-Type"] in JSON_MIME_TYPES:
            try:
                self.req_body = json.loads(
                    self.decode_argument(self.request.body)
                )
            except json.decoder.JSONDecodeError as err:
                # when parsing invalid JSON, inform the user of where to fix the invalid JSON
                self.set_status(400)
                self.finish({ "message": str(err) })

    @coroutine
    def get(self):
        users = list(self.database.users.find({}, {"_id": 0}))
        self.write(json.dumps(users))

    @coroutine
    def post(self):
        self.write(json.dumps(self.req_body))
