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
    def test_valid_json(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(
            self.get_url("/customers"),
            raise_error=False,
            method="POST",
            body='{"hello":"world"}'
            )
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, bytes('{"hello": "world"}', "utf-8"))