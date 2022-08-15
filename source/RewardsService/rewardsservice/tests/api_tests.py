import unittest
import requests

class TestEndPointOne(unittest.TestCase):
    def test_malformed_email(self):
        expected = "not a valid email"
        result = requests.post("http://localhost:7050/endpoint_one?email=reddd6@7&points=1").text
        self.assertEqual(result, expected)
    
    def test_point_not_number(self):
        expected = "points were not a number"
        result = requests.post("http://localhost:7050/endpoint_one?email=reddd6@7.org&points=a").text
        self.assertEqual(result, expected)

class TestEndPointtwo(unittest.TestCase):
    def test_malformed_email(self):
        expected = "not a valid email"
        result = requests.get("http://localhost:7050/endpoint_two?email=reddd6@7").text
        self.assertEqual(result, expected)

class TestEndPointThree(unittest.TestCase):
    def test_post_rejected(self):
        expected = 405
        result = requests.post("http://localhost:7050/endpoint_three").status_code
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()