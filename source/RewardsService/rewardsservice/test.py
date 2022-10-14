
from url_patterns import url_patterns
from tornado.testing import AsyncHTTPTestCase, AsyncHTTPClient, gen_test, main
from app import App

class ValidationTestsCustomersPost(AsyncHTTPTestCase):
    app = App(url_patterns)

    def get_app(self):
        return self.app

    #test to check valididity of json
    @gen_test
    def json_test(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body="{"
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Invalid JSON","utf-8"))

    #test to check if email address is missing
    @gen_test
    def email_address_missing_test(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"hello":"world"}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Missing required field 'email_address'", "utf-8"))

    #test to check if order total is not rounded when email address is provided
    @gen_test
    def email_address_provided_order_total_not_rounded_test(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu", "order_total": 100.0001}'
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("'order_total' must be a number with no more than two values after the decimal point", "utf-8"))

    # test to check if order total is not provided when email address is provided
    @gen_test
    def email_address_provided_order_total_missing_test(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu"}'
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Missing required field 'order_total'", "utf-8"))

    # test to check if order total is not rounded when email address is provided
    @gen_test
    def email_address_provided_order_total_not_number_test(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"email_address":"loma@sas.upenn.edu", "order_total": "hello"}'
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("'order_total' must be a number", "utf-8"))

    # test to check if UTF-8 encoding is done
    @gen_test
    def test_not_encoded_body(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body= bytes("{}","cp500")
            )
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, bytes("Request body must be utf-8 encoded","utf-8"))
