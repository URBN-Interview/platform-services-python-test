"""
Testing out post and get of rewards handling using python requests
"""

import unittest
import json
import requests

class TestRewardHandler(unittest.TestCase):
    
    # test post of reward handler
    def post_reward_handler(self):
        customer = {
            "email": "test@test.com",
            "total": 100
        }

        json_request = json.dumps(customer)

        response = requests.post(
            "http://localhost:7050/rewards", 
            json_request,
            headers={
                "Content-type": "application/json",
                "Accept": "text/plain"
            }
        )

        print(response)

        self.assertEqual(200, response.status_code)
        self.assertEqual({"success": True}, response.json())

if __name__ == '__main__':
    unittest.main()