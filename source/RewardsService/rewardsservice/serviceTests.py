from tornado.testing import AsyncTestCase, gen_test
from tornado.web import Application
from tornado.httpserver import HTTPRequest
from unittest.mock import Mock
from tornado.httputil import url_concat

from handlers import customer_handler
from handlers import customers_handler
from handlers import processOrder_handler


class TestAllHandlers(AsyncTestCase):
    @gen_test
    def test_missing_email_customers(self):
        mock_application = Mock(spec=Application)
        params = {"email": ""}
        url = url_concat("/customer/", params)

        payload_request = HTTPRequest(
            method='GET', uri=url, headers=None, body=None
        )
        handler = customer_handler(mock_application, payload_request)
        with self.assertRaises(400):
            yield handler.get()

    @gen_test
    def test_invalid_email_customers(self):
        params = {"email": "test.test.com"}
        url = url_concat("/customer/", params)
        mock_application = Mock(spec=Application)
        payload_request = HTTPRequest(
            method='GET', uri=url, headers=None, body=None
        )
        handler = customer_handler(mock_application, payload_request)
        with self.assertRaises(400):
            yield handler.get()

    @gen_test
    def test_missing_total(self):
        params = {"email": "test.test.com", "order_total": ""}
        url = url_concat("/processOrder/", params)

        mock_application = Mock(spec=Application)
        payload_request = HTTPRequest(
            method='POST', uri=url, headers=None, body=None
        )
        handler = processOrder_handler(mock_application, payload_request)
        with self.assertRaises(400):
            yield handler.get()
    

    @gen_test
    def test_invalid_email(self):
        params = {"email": "test.test.com", "order_total": ""}
        url = url_concat("/processOrder/", params)

        mock_application = Mock(spec=Application)
        payload_request = HTTPRequest(
            method='POST', uri=url, headers=None, body=None
        )
        handler = processOrder_handler(mock_application, payload_request)
        with self.assertRaises(400):
            yield handler.get()