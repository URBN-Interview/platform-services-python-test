import json
import tornado.testing

from tornado.testing import AsyncTestCase, AsyncHTTPClient
from pymongo import MongoClient


class TestEndpoints(AsyncTestCase):
    @tornado.testing.gen_test
    def test_get_customers(self):
        db_client = MongoClient("mongodb", 27017)
        db = db_client["Rewards"]
        expected = list(db.customers.find({}, {"_id": 0}))

        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:7050/get-customers")
        # Testing if contents of customers collection return
        self.assertEqual(expected, json.loads(response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_get_customer_data(self):
        expected = []
        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:7050/get-customer-data?email=test123")

        self.assertEqual(expected, json.loads(response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_rewards_status_new(self):
        # test making a purchase with a new email address
        expected = [{
            "email": "new_test@gmail.com",
            "points": 410,
            "tier": "D",
            "tierName": "30% off purchase",
            "nextTier": "E",
            "nextTierName": "40% off purchase",
            "nextTierProgress": 0.1
        }]
        # delete any existing instance of the test email
        db_client = MongoClient("mongodb", 27017)
        db = db_client["Rewards"]
        db['customers'].delete_many({"email": "new_test@gmail.com"})

        client = AsyncHTTPClient()
        post_response = yield client.fetch("http://localhost:7050/rewards-status?"
                                           "email=new_test@gmail.com&order-total=410")
        get_response = yield client.fetch("http://localhost:7050/get-customer-data?email=new_test@gmail.com")

        self.assertEqual(expected, json.loads(get_response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_rewards_status_existing(self):
        # test making a purchase with an existing email address. Should only update the points and tier if necessary
        # test making a purchase with a new email address
        expected = [{
            "email": "new_test@gmail.com",
            "points": 3,
            "tier": "D",
            "tierName": "30% off purchase",
            "nextTier": "E",
            "nextTierName": "40% off purchase",
            "nextTierProgress": 0.1
        }]
        # delete any existing instance of the test email
        db_client = MongoClient("mongodb", 27017)
        db = db_client["Rewards"]
        db.customers.delete_all({"email": "new_test@gmail.com"})
        db.customers.insert(expected[0])

        client = AsyncHTTPClient()
        post_response = yield client.fetch("http://localhost:7050/rewards-status?"
                                           "email=new_test@gmail.com&order-total=410")
        get_response = yield client.fetch("http://localhost:7050/get-customer-data?email=new_test@gmail.com")

        self.assertDictEqual(expected[0], json.loads(get_response.body.decode('utf-8')[0]))
