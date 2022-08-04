import unittest
import requests

from unittest.mock import patch

class TestRewardsDataHandler(unittest.TestCase):
    def test_submit_valid_order(self):
        response = requests.post("http://localhost:7050/rewards_data", {
            "email_address": "test@test.com",
            "order_total": "100.80"
        })
        self.assertEqual(response.status_code, 200)

        response = requests.get("http://localhost:7050/rewards_data?email=test@test.com")
        self.assertEqual(response.status_code, 200)
    
    def test_submit_invalid_email(self):
        response = requests.post("http://localhost:7050/rewards_data", {
            "email_address": "test",
            "order_total": "100.80"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason, "invalid email address")
    
    def test_submit_invalid_total(self):
        response = requests.post("http://localhost:7050/rewards_data", {
            "email_address": "test@test.com",
            "order_total": "test"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.reason, "order total must be a number")
    
    def test_submit_blank_input(self):
        response = requests.post("http://localhost:7050/rewards_data", {})
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_rewards_data(self):
        response = requests.get("http://localhost:7050/rewards_data")
        self.assertEqual(response.status_code, 200)
    
    def test_get_invalid_customer(self):
        response = requests.get("http://localhost:7050/rewards_data?email=test")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.reason, "customer not found: test")

if __name__ == '__main__':
    unittest.main()
