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
    split = total.split(".")
    if len(split) == 1:
        return [split[0], None]
    return split

def get_rewards_tier_idx(total, num_tiers):
    dollars = "{0}".format(parse_purchase_total(total)[0])
    dollar_magnitude = len(dollars)
    if dollar_magnitude > 2:
        return min(int(dollars[0:dollar_magnitude-2]), num_tiers) - 1
    return None

class OrdersHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.database = MongoClient("mongodb", 27017)["Rewards"]

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, DELETE, OPTIONS")

    def report_error(self, error_message):
        self.set_status(400)
        self.finish({ "message": error_message })

    @coroutine
    def options(self, *args):
        self.set_status(204)
        self.finish

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
        data = None
        email = self.get_argument("email_address", None)
        if email is None:
            data = list(self.database.users.find({}, { "_id": 0 }))
        else:
            query_result = self.database.users.find_one({ "email_address": email }, { "_id": 0 })
            if query_result is not None:
                data = query_result
            else:
                data = []
        self.write(json.dumps(data))

    @coroutine
    def post(self):
        email = self.request.body["email_address"]
        [dollars, _] = parse_purchase_total(self.request.body["purchase_total"])
        current_user_record = self.database.users.find_one({ "email_address": email })
        points_sum = int(dollars)
        if current_user_record is not None:
            points_sum += int(current_user_record["rewards_points"])
        rewards = list(self.database.rewards.find({}, {"_id": 0}))
        rewards_len = len(rewards)

        current_idx = get_rewards_tier_idx("{0}".format(points_sum), rewards_len)
        current_tier = {}
        try:
            current_tier = rewards[current_idx]
        except IndexError:
            pass
        except TypeError:
            pass

        next_tier = {}
        next_points = rewards[0]["points"]
        tier_progress = "0%"
        try:
            next_idx = min(current_idx + 1, rewards_len)
            if next_idx == rewards_len:
                next_tier = {}
                next_points = rewards[-1]["points"]
                tier_progress = "100%"
            else:
                next_tier = rewards[next_idx]
                next_points = next_tier["points"]
        except IndexError:
            next_tier = rewards[0]
            next_points = next_tier["points"]
            pass
        except TypeError:
            next_tier = rewards[0]
            next_points = next_tier["points"]
            pass
        
        tier_progress = "{:.2f}%".format(points_sum / next_points * 100)
        new_user_record = {
            "email_address": email,
            "rewards_points": points_sum,
            "next_tier_progress": tier_progress,
            "current_tier": current_tier,
            "next_tier": next_tier,
        }
        if current_user_record is not None:
            self.database.users.replace_one({"_id": current_user_record["_id"]}, new_user_record)
        else:
            self.database.users.insert_one(new_user_record)
        self.finish()

    @coroutine
    def delete(self):
        result = self.database.users.delete_many(
            { "email_address": self.request.body["email_address"] }
        )
        self.write({ "message": "Number of rows affected: {0}".format(result.deleted_count) })
