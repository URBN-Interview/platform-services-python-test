from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from handlers.rewards_handler import RewardsHandler
from handlers.customer_rewards_handler import CustomerRewardsHandler

class TestrewardsService(AsyncHTTPTestCase):
    request_body = b'{"email": "jdoe2@example.com","orderTotal": 5.8}'
    
    def get_app(self):
        return Application([
                (r'/rewards', RewardsHandler),
                (r'/customerrewards', CustomerRewardsHandler),
                (r"/customerrewards/?(.*)?", CustomerRewardsHandler),
            ])

    def test_should_return_ok_for_get_all(self):
        response = self.fetch("/customerrewards", method="GET")
        self.assertEqual(200, response.code)

    def test_should_return_ok_for_post_new_user(self):
        response = self.fetch("/customerrewards", method="POST", body=self.request_body)
        self.assertEqual(201, response.code)
