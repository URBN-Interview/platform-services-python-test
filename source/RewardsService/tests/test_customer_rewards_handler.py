from collections import namedtuple
import unittest
from unittest.mock import patch, Mock

import tornado.testing
from tornado.testing import AsyncHTTPTestCase, main


class TestCustomerRewards(AsyncHTTPTestCase):

    def get_app(self):
        MockDB = namedtuple('MockDB', ['customer_rewards'])
        self.db = Mock(return_value=MockDB)
        # return app

    def test_get_by_email_found(self):
        self.db.find_one = Mock(return_value={'emailAddress': 'foo@bar.com'})
        response = self.fetch("/customer-rewards/foo@bar.com", method="GET")
        self.assertEqual(response.code, 200)

    def test_get_by_email_not_found(self):
        self.db.find_one = Mock(return_value=None)
        response = self.fetch("/customer-rewards/foo@bar.com", method="GET")
        self.assertEqual(response.code, 404)


if __name__ == '__main__':
    tornado.testing.main()
