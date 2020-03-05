import tornado.testing
import tornado.httpclient
from ..model.customer import Customer

app = 'http://localhost:7050'
mockCustomer = Customer(email="test@email.com", orderTotal='100.00')

class MyTestCase(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_create_order_success(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('%s/order?email=%s&orderTotal=%s' % (app, mockCustomer.email, mockCustomer.orderTotal), self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

class MyTestCase2(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_update_customer(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('%s/order?email=%s&orderTotal=%s' % (app, mockCustomer.email, mockCustomer.orderTotal), self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

class MyTestCase3(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_get_customer(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch('%s/customer?email=%s' % (app, mockCustomer.email), self.stop)
        response = self.wait()
        self.assertEqual(200, response.code)

class MyTestCase4(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_http_fetch(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('%s/customers'%(app), self.stop)
        response = self.wait()
        self.assertGreater(len(response.body), 0)
        self.assertEqual(200, response.code)

class MyTestCase5(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_create_order_email_validate_fail(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('%s/order?email=%s&orderTotal=%s' % (app, 'email', mockCustomer.orderTotal), self.stop)
        response = self.wait()
        self.assertEqual(500, response.code)

class MyTestCase6(tornado.testing.AsyncTestCase):
    @tornado.testing.gen_test
    def test_create_order_total_order_validate_fail(self):
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch('%s/order?email=%s&orderTotal=%s' % (app, mockCustomer.email, '10.001'), self.stop)
        response = self.wait()
        self.assertEqual(500, response.code)