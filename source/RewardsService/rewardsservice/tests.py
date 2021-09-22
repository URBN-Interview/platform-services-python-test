from tornado.testing import AsyncTestCase, gen_test
from tornado.web import Application
from tornado.httpserver import HTTPRequest
from unittest.mock import Mock


class TestSomeHandler(AsyncTestCase):

    @gen_test
    def test_rewards_count(self):
        payload_request = HTTPRequest(
            method='GET', uri='/rewards', headers=None, body=None
        )
        handler = SomeHandler(mock_applciation, payload_request)
        with self.assertRaises(ValueError):
            yield handler.get()
