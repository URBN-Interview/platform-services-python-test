import json
import re
import tornado.web

from pymongo import MongoClient
from tornado.gen import coroutine

from settings import JSON_MIME_TYPES

# if a REST verb needs to be validated for data being present, add it here
VALIDATED_VERBS = ["POST", "PUT"]

ERROR_MESSAGES = {
    "required": {
        "email_address": "The user's email_address is missing and is a required field",
        "purchase_total": "The user's purchase_total is missing and is a required field",
    },
    "validation": {
        "purchase_total": "The purchase_total is not a valid number. A valid number is classified as matching the regex '[0-9]+(\\.[0-9]{2})?'"
    },
}

VALIDATORS = {
    "purchase_total": re.compile("^\\d+(\\.\\d{2})?$"),
}

def parse_purchase_total(total):
    dollars, cents = total.split(".")
    return (dollars, cents)

class UsersHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.database = MongoClient("mongodb", 27017)["Rewards"]
    
    def report_error(self, error_message):
        self.set_status(400)
        self.finish({ "message": error_message })

    @coroutine
    def prepare(self):
        content_type = self.request.headers.get("Content-Type")
        if content_type and content_type in JSON_MIME_TYPES:
            try:
                self.request.body = json.loads(self.decode_argument(self.request.body))
            except json.decoder.JSONDecodeError as err:
                # when parsing invalid JSON, inform the user of where to fix the invalid JSON
                self.report_error(str(err))
        if self.request.method in VALIDATED_VERBS:
            # validate that all necessary parameters have been passed in the request body
            data_keys = list(self.request.body.keys())
            validated_keys = list(VALIDATORS.keys())
            for field in list(ERROR_MESSAGES["required"].keys()):
                if field not in data_keys:
                    self.report_error(ERROR_MESSAGES["required"][field])
                if field in validated_keys:
                    if not VALIDATORS[field].match(self.request.body[field]):
                        self.report_error(ERROR_MESSAGES["validation"][field])

    @coroutine
    def get(self):
        users = list(self.database.users.find({}, {"_id": 0}))
        self.write(json.dumps(users))

    @coroutine
    def post(self):
        email = self.request.body["email_address"]
        purchase_total = self.request.body["purchase_total"]
        previous_purchases = list(self.database.users.find({ "email_address": email }))
        self.write(json.dumps(previous_purchases))
