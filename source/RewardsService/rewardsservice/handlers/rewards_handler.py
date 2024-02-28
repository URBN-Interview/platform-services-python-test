import json
import tornado.web

from tornado.gen import coroutine

from rewardsservice.utils import ComputationUtils


class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        rewards = ComputationUtils.compute_rewards()
        self.write(json.dumps(rewards))


class EmailHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        email_address = self.get_argument('email_address', None)
        user_details = ComputationUtils.compute_user_details_for_email_address(email_address)
        self.write(json.dumps(user_details))


class OrderHandler(tornado.web.RequestHandler):

    @coroutine
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        email_address = data.get('email_address', '')
        order_total = data.get('order_total', 0)
        success, message = ComputationUtils.add_order(email_address=email_address, order_total=order_total)
        self.write({'message': message, "success": success})

