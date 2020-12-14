from urllib import parse
from tornado.testing import AsyncHTTPTestCase
from tornado.options import options
from rewardsservice.app import app
from rewardsservice.url_patterns import url_patterns


class TestHttpResponse(AsyncHTTPTestCase):

    def get_app(self):
        return app.make_app(url_patterns)

    def get_http_port(self):
        return options.port

    def test_post_customer_rewards_returns_200(self):
        response = self.fetch('/calculate_rewards', method="POST", body=parse.urlencode({'email': 'test_user@gmail.com',
                                                                                         'order_total': '50.00'}))
        self.assertEqual(response.code, 200)

    def test_get_customer_rewards_returns_200(self):
        response = self.fetch('/customer_rewards?email=test_user@gmail.com', method="GET")
        self.assertEqual(response.code, 200)

    def test_get_all_customer_data_returns_200(self):
        response = self.fetch('/customer_data', method="GET")
        self.assertEqual(response.code, 200)

    def test_get_customer_rewards_user_not_found_returns_404(self):
        response = self.fetch('/customer_rewards?email=unknown_user@gmail.com', method="GET")
        self.assertEqual(response.code, 404)

    def test_get_customer_rewards_invalid_email_returns_400(self):
        response = self.fetch('/customer_rewards?email=gmail.com', method="GET")
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'<html><body>Invalid email</body></html>')

    def test_post_customer_rewards_invalid_total_returns_400(self):
        response = self.fetch('/calculate_rewards', method="POST", body=parse.urlencode({'email': 'test_user@gmail.com',
                                                                                         'order_total': 'twenty'}))
        self.assertEqual(response.code, 400)
        self.assertEqual(response.body, b'<html><body>Order total is not a valid number</body></html>')
