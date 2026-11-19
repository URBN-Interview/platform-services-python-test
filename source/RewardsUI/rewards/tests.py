from unittest import mock

import requests
from django.test import SimpleTestCase
from django.urls import reverse

from rewards.clients.rewards_service_client import RewardsServiceClient, RewardsServiceError
from rewards.views import RewardsView

TIERS = [
    {"tier": "A", "rewardName": "5% off purchase", "points": 100},
    {"tier": "B", "rewardName": "10% off purchase", "points": 200},
]
CUSTOMER = {
    "email": "customer01@gmail.com",
    "points": 100,
    "tier": "A",
    "tierName": "5% off purchase",
    "nextTier": "B",
    "nextTierName": "10% off purchase",
    "nextTierProgress": 0.5,
}
OTHER_CUSTOMER = dict(CUSTOMER, email="customer02@gmail.com", points=40, tier=None, tierName=None,
                      nextTier="A", nextTierName="5% off purchase", nextTierProgress=0.4)


class RewardsViewTest(SimpleTestCase):

    def setUp(self):
        self.client_mock = mock.Mock(spec=RewardsServiceClient)
        self.client_mock.get_rewards.return_value = TIERS
        self.client_mock.get_customers.return_value = [CUSTOMER, OTHER_CUSTOMER]
        self.client_mock.get_customer.return_value = CUSTOMER
        patcher = mock.patch.object(RewardsView, "rewards_service_client", self.client_mock)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.url = reverse("rewards")

    def test_dashboard_lists_tiers_and_all_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10% off purchase")
        self.assertContains(response, "customer01@gmail.com")
        self.assertContains(response, "customer02@gmail.com")
        self.assertContains(response, "50%")
        self.client_mock.get_customers.assert_called_once_with()

    def test_filter_by_email(self):
        response = self.client.get(self.url, {"email": "Customer01@Gmail.com"})
        self.assertEqual(response.status_code, 200)
        self.client_mock.get_customer.assert_called_once_with("customer01@gmail.com")
        self.client_mock.get_customers.assert_not_called()
        self.assertContains(response, "customer01@gmail.com")
        self.assertNotContains(response, "customer02@gmail.com")
        self.assertContains(response, "Show all")

    def test_filter_with_no_match(self):
        self.client_mock.get_customer.return_value = None
        response = self.client.get(self.url, {"email": "nobody@x.com"})
        self.assertContains(response, "No rewards found for nobody@x.com")

    def test_filter_with_invalid_email_shows_error(self):
        response = self.client.get(self.url, {"email": "not-an-email"})
        self.assertContains(response, "Enter a valid email address")
        self.client_mock.get_customer.assert_not_called()

    def test_submit_order_redirects_with_success_message(self):
        self.client_mock.add_order.return_value = CUSTOMER
        response = self.client.post(self.url, {"email": "customer01@gmail.com", "order_total": "100.80"}, follow=True)
        self.client_mock.add_order.assert_called_once_with("customer01@gmail.com", "100.80")
        self.assertRedirects(response, self.url)
        self.assertContains(response, "Order added for customer01@gmail.com. They now have 100 points (tier A).")

    def test_submit_invalid_order_shows_field_errors(self):
        response = self.client.post(self.url, {"email": "bad", "order_total": "-3"})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Enter a valid email address", status_code=400)
        self.assertContains(response, "greater than or equal to 0", status_code=400)
        self.client_mock.add_order.assert_not_called()

    def test_submit_order_service_error(self):
        self.client_mock.add_order.side_effect = RewardsServiceError("The rewards service is unavailable.")
        response = self.client.post(self.url, {"email": "c@x.com", "order_total": "10"})
        self.assertEqual(response.status_code, 502)
        self.assertContains(response, "The rewards service is unavailable.", status_code=502)

    def test_service_down_still_renders_page(self):
        self.client_mock.get_rewards.side_effect = RewardsServiceError("down")
        self.client_mock.get_customers.side_effect = RewardsServiceError("down")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Could not load reward tiers: down")
        self.assertContains(response, "Could not load customer rewards: down")


class RewardsServiceClientTest(SimpleTestCase):

    def setUp(self):
        self.session = mock.Mock(spec=requests.Session)
        self.client_under_test = RewardsServiceClient("http://svc:7050/", session=self.session)

    def respond(self, status, payload):
        response = mock.Mock(ok=200 <= status < 300, status_code=status)
        response.json.return_value = payload
        self.session.request.return_value = response

    def test_add_order_posts_json(self):
        self.respond(201, CUSTOMER)
        self.assertEqual(self.client_under_test.add_order("c@x.com", "10.50"), CUSTOMER)
        self.session.request.assert_called_once_with(
            "POST", "http://svc:7050/orders", timeout=5, json={"email": "c@x.com", "orderTotal": "10.50"},
        )

    def test_get_customer_url_encodes_email(self):
        self.respond(200, CUSTOMER)
        self.client_under_test.get_customer("a+b@x.com")
        self.session.request.assert_called_once_with("GET", "http://svc:7050/customers/a%2Bb%40x.com", timeout=5)

    def test_get_customer_returns_none_on_404(self):
        self.respond(404, {"error": {"code": 404, "message": "not found"}})
        self.assertIsNone(self.client_under_test.get_customer("a@x.com"))

    def test_error_message_from_service(self):
        self.respond(400, {"error": {"code": 400, "message": "'orderTotal' must be a number"}})
        with self.assertRaises(RewardsServiceError) as ctx:
            self.client_under_test.add_order("a@x.com", "x")
        self.assertEqual(ctx.exception.message, "'orderTotal' must be a number")
        self.assertEqual(ctx.exception.status_code, 400)

    def test_connection_error(self):
        self.session.request.side_effect = requests.ConnectionError()
        with self.assertRaises(RewardsServiceError) as ctx:
            self.client_under_test.get_customers()
        self.assertIn("unavailable", ctx.exception.message)
