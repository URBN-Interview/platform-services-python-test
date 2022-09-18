import unittest
import requests
import json

url = 'http://localhost:7050/customerRewards'


class TestCustomerRewardsAPI(unittest.TestCase):

    def test_post_basic(self):
        payload = {'email': 'a@b.com', 'order_total': 203}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(url, data=json.dumps(
            payload), headers=headers)
        self.assertEqual(result.status_code, 200)

    def test_post_email_error(self):
        payload = {'email': 'a@b', 'order_total': 203}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(url, data=json.dumps(
            payload), headers=headers)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"message": "Invalid email"}')

    def test_post_order_total_error(self):
        payload = {'email': 'a@b.com', 'order_total': 'wer'}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        result = requests.post(url, data=json.dumps(
            payload), headers=headers)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"message": "Invalid order total"}')

    def test_get_basic(self):
        result = requests.get(url)
        self.assertEqual(result.status_code, 200)

    def test_get_basic_email(self):
        params = {'email': 'a@b.com'}
        result = requests.get(url, params=params)
        self.assertEqual(result.status_code, 200)

    def test_get_basic_email_error(self):
        params = {'email': 'a@b'}
        result = requests.get(url, params=params)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result.text, '{"message": "Invalid email"}')


if __name__ == '__main__':
    unittest.main()
