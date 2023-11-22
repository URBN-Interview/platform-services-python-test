import json
import tornado.testing

from tornado.testing import AsyncTestCase, AsyncHTTPClient

"""
Note that these tests require the mongodb customers collection to be completely clear before running. 
If I had more time to complete this step, I would add mocks to emulate the mongodb server and test the endpoints
against that.
"""


class TestEndpoints(AsyncTestCase):

    @tornado.testing.gen_test
    def test_get_customer_data(self):
        # tests getting a nonexistent customer email
        expected = []
        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:7050/get-customer-data?email=test123")

        self.assertEqual(expected, json.loads(response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_add_order_1(self):
        # test making a purchase with a new email address
        expected = [{
            "email": "new_test@gmail.com",
            "points": 410,
            "tier": "D",
            "tierName": "20% off purchase",
            "nextTier": "E",
            "nextTierName": "25% off purchase",
            "nextTierProgress": 0.1
        }]

        client = AsyncHTTPClient()
        post_response = yield client.fetch("http://localhost:7050/add-order?"
                                           "email=new_test@gmail.com&order-total=410")
        # this test doubles as a test for the get-customer-data endpoint with an existing email
        get_response = yield client.fetch("http://localhost:7050/get-customer-data?email=new_test@gmail.com")

        self.assertEqual(expected, json.loads(get_response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_add_order_2(self):
        # test making a purchase with an existing email address. Should only update the points and tier if necessary
        # test making a purchase with a new email address
        expected = [{
            "email": "new_test@gmail.com",
            "points": 820,
            "tier": "H",
            "tierName": "40% off purchase",
            "nextTier": "I",
            "nextTierName": "45% off purchase",
            "nextTierProgress": 0.2
        }]

        client = AsyncHTTPClient()
        post_response = yield client.fetch("http://localhost:7050/add-order?"
                                           "email=new_test@gmail.com&order-total=410")
        # this test doubles as a test for the get-customer-data endpoint with an existing email
        get_response = yield client.fetch("http://localhost:7050/get-customer-data?email=new_test@gmail.com")

        self.assertEqual(expected, json.loads(get_response.body.decode('utf-8')))

    @tornado.testing.gen_test
    def test_get_customers(self):
        # tests the get_customers endpoint. Should yield the object we inserted in add_order
        expected = [{
            "email": "new_test@gmail.com",
            "points": 820,
            "tier": "H",
            "tierName": "40% off purchase",
            "nextTier": "I",
            "nextTierName": "45% off purchase",
            "nextTierProgress": 0.2
        }]
        client = AsyncHTTPClient()
        response = yield client.fetch("http://localhost:7050/get-customers")
        # Testing if contents of customers collection return
        self.assertEqual(expected, json.loads(response.body.decode('utf-8')))
