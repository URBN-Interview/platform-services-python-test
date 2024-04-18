import json
import tornado.web
from pymongo import MongoClient
from tornado.gen import coroutine
import pandas as pd


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        rewards = list(db.rewards.find({}, {"_id": 0}))
        self.write(json.dumps(rewards))


class OrderDataHandler(tornado.web.RequestHandler):
    @coroutine
    def post(self):
        data = json.loads(self.request.body.decode())
        email_address = data.get("email_address", None)
        order_total = data.get("order_total", None)
        order_point = int(order_total)
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        df = pd.DataFrame(list(db.rewards.find({}, {"_id": 0})))
        point_lists = list(df["points"])
        point_lists.append(1100)
        df["points_range"] = pd.cut(df["points"], point_lists, right=False)
        # row_in_range = df[[order_point in i for i in df['points_range']]].index[0]
        orderrewards = db["order_rewards"]
        cursor = orderrewards.find({"email_address": email_address})
        if cursor.count():
            order_point = cursor[0]["reward_points"] + order_point
            range_row = df[[order_point in i for i in df["points_range"]]]
            index_range = range_row.index[0]
            range_row_interval = range_row["points_range"].values[0]
            next_range_row = df.loc[index_range + 1]
            customer_data_reward = {
                # "email_address": email_address,  # #the customer's email address (ex. "customer01@gmail.com")
                "reward_points": order_point,  # the customer's rewards points (ex. 100)
                "reward_tier": range_row["tier"].values[
                    0
                ],  # the rewards tier the customer has reached (ex. "A")
                "reward_tier_name": range_row["rewardName"].values[
                    0
                ],  # the name of the rewards tier (ex. "5% off purchase")
                "next_reward_tier": next_range_row[
                    "tier"
                ],  # the next rewards tier the customer can reach (ex. "B")
                "next_reward_tier_name": next_range_row[
                    "rewardName"
                ],  # the name of next rewards tier (ex. "10% off purchase")
                "next_reward_tier_progress": round(
                    (
                        (next_range_row["points"] - order_point)
                        / next_range_row["points"]
                    )
                    * 100,
                    2,
                ),  # the percentage the customer is away from reaching the
            }
            orderrewards.update_one(
                {"email_address": email_address}, {"$set": customer_data_reward}
            )
        else:
            range_row = df[[order_point in i for i in df["points_range"]]]
            index_range = range_row.index[0]
            range_row_interval = range_row["points_range"].values[0]
            next_range_row = df.loc[index_range + 1]

            customer_data = {
                "email_address": email_address,  # #the customer's email address (ex. "customer01@gmail.com")
                "reward_points": order_point,  # the customer's rewards points (ex. 100)
                "reward_tier": range_row["tier"].values[
                    0
                ],  # the rewards tier the customer has reached (ex. "A")
                "reward_tier_name": range_row["rewardName"].values[
                    0
                ],  # the name of the rewards tier (ex. "5% off purchase")
                "next_reward_tier": next_range_row[
                    "tier"
                ],  # the next rewards tier the customer can reach (ex. "B")
                "next_reward_tier_name": next_range_row[
                    "rewardName"
                ],  # the name of next rewards tier (ex. "10% off purchase")
                "next_reward_tier_progress": round(
                    (
                        (next_range_row["points"] - order_point)
                        / next_range_row["points"]
                    )
                    * 100,
                    2,
                ),  # the percentage the customer is away from reaching the
            }
            orderrewards.insert_one(customer_data)
        self.write(
            json.dumps(
                {
                    "message": "for user "
                    + email_address
                    + " order data has been inserted"
                }
            )
        )


class CusotmerRewardDataHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        # data = json.loads(self.request.body.decode())
        email_address = self.request.query_arguments["email"][0]
        email_address = email_address.decode()
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        orderrewards = db["order_rewards"]
        cursor = orderrewards.find({"email_address": email_address})

        self.write(json.dumps({i: cursor[0][i] for i in cursor[0] if i != "_id"}))


class AllCusotmerRewardDataHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        client = MongoClient("mongodb", 27017)
        db = client["Rewards"]
        orderrewards = db["order_rewards"]
        orderrewards_list = list(orderrewards.find({}, {"_id": 0}))
        self.write(json.dumps(orderrewards_list))
