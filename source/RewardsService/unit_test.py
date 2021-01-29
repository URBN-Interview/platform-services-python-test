import ast
import unittest
import requests

from pymongo import MongoClient


class RewardServiceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_url = "http://localhost:7050"
        cls.rewards_url = cls.base_url + "/rewards"
        cls.customer_url = cls.base_url + "/me/rewards"
        cls.list_rewards_url = cls.base_url + "/rewards/customers"

        client = MongoClient("localhost", 27017)
        cls.db = client["Rewards"]

    def setUp(self):
        self.email_address = "stantest@urbn.com"
        self.order_total = 180

        self.db.customer_rewards.delete_many({"emailAddress": self.email_address})

    def test_post_rewards(self):
        response = requests.post(self.rewards_url,
                                 params={"email_address": self.email_address, "order_total": self.order_total})
        self.assertEqual(200, response.status_code)
        response_body = ast.literal_eval(response.content.decode("utf-8"))

        self.assertEqual(self.email_address, response_body.get("emailAddress"))
        self.assertEqual(self.order_total, response_body.get("points"))
        self.assertEqual("A", response_body.get("tier"))
        self.assertEqual("B", response_body.get("nextTier"))

    def test_updating_existing_user_reward(self):
        requests.post(self.rewards_url, params={"email_address": self.email_address, "order_total": self.order_total})
        response = requests.post(self.rewards_url,
                                 params={"email_address": self.email_address, "order_total": self.order_total})

        self.assertEqual(200, response.status_code)
        response_body = ast.literal_eval(response.content.decode("utf-8"))

        self.assertEqual(self.email_address, response_body.get("emailAddress"))
        self.assertEqual(self.order_total + self.order_total, response_body.get("points"))
        self.assertEqual("C", response_body.get("tier"))
        self.assertEqual("D", response_body.get("nextTier"))

    def test_post_rewards_without_email_address_params(self):
        response = requests.post(self.rewards_url, params={"order_total": self.order_total})
        response_body = ast.literal_eval(response.content.decode("utf-8"))
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(response_body, {'message': 'Please provide email address and order total', 'code': 'VALIDATION_ERROR'})

    def test_post_rewards_without_order_total_params(self):
        response = requests.post(self.rewards_url, params={"email_address": self.email_address})
        response_body = ast.literal_eval(response.content.decode("utf-8"))
        self.assertEqual(400, response.status_code)
        self.assertDictEqual(response_body, {'message': 'Please provide email address and order total', 'code': 'VALIDATION_ERROR'})

    def test_get_customers(self):
        requests.post(self.rewards_url,
                                 params={"email_address": self.email_address, "order_total": self.order_total})
        response = requests.get(self.customer_url, params={"email_address":self.email_address})
        self.assertEqual(200, response.status_code)

        response_body = ast.literal_eval(response.content.decode("utf-8"))
        self.assertEqual(self.email_address, response_body.get("emailAddress"))

        for key in ["_id", "rewardTierName", "emailAddress", "tier", "points", "nextTier", "progress"]:
            self.assertIn(key, response_body)

    def test_get_customers_without_email_address(self):
        response = requests.get(self.customer_url)
        self.assertEqual(400, response.status_code)

    def test_get_list_of_rewards(self):
        response = requests.get(self.list_rewards_url)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
