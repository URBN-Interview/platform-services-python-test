from app import App
from url_patterns import url_patterns
from tornado.testing import AsyncHTTPTestCase, AsyncHTTPClient, gen_test, main

class PostCustomersTests(AsyncHTTPTestCase):
    app = App(url_patterns)

    def get_app(self):
        return self.app

    @gen_test
    def test_body_not_utf8_encoded(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body= bytes("{}","cp500")
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Request body must be utf-8 encoded","utf-8"))

    @gen_test
    def test_invalid_json(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body="{"
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Invalid JSON","utf-8"))

    @gen_test
    def test_missing_email_address(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"hello":"world"}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Missing required field 'email_address'", "utf-8"))

    @gen_test
    def test_have_email_address_missing_order_total(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu"}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Missing required field 'order_total'", "utf-8"))

    @gen_test
    def test_have_email_address_order_total_is_not_number(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu", "order_total": "hello"}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("'order_total' must be a number", "utf-8"))

    @gen_test
    def test_have_email_address_order_total_needs_rounding(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu", "order_total": 100.0001}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("'order_total' must be a number with no more than two values after the decimal point", "utf-8"))

    # @gen_test
    # def test_success_have_all_fields_order_total_is_int(self):
    #     client = AsyncHTTPClient()
    #     response = yield client.fetch(
    #         self.get_url("/customers"),
    #         raise_error=False,
    #         method="POST",
    #         body='{"email_address":"loma@sas.upenn.edu", "order_total": 100}'
    #         )
    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response.body, bytes("email_address: loma@sas.upenn.edu, order_total: 100.00", "utf-8"))

    # @gen_test
    # def test_success_have_all_fields_order_total_is_float(self):
    #     client = AsyncHTTPClient()
    #     response = yield client.fetch(
    #         self.get_url("/customers"),
    #         raise_error=False,
    #         method="POST",
    #         body='{"email_address":"loma@sas.upenn.edu", "order_total": 100.00}'
    #         )
    #     self.assertEqual(response.code, 200)
    #     self.assertEqual(response.body, bytes("email_address: loma@sas.upenn.edu, order_total: 100.00", "utf-8"))

