"""
Test of customer handler
"""
import unittest
import json
import requests

class TestCustomerHandler(unittest.TestCase):
    def test_get_customer(self):
        response = requests.get(
            "http://localhost:7050/customers", 
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain"
            }
        )

        print(response.json())

        self.assertEqual(200, response.status_code)

    def test_post_customer(self):
        query = {"email": "test@test.com"}
        
        json_request = json.dumps(query)

        response = requests.post(
            "http://localhost:7050/customers", 
            json_request,
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain"
            }
        )

        print(response)

        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()