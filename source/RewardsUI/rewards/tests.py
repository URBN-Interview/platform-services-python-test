from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rewards.clients.rewards_service_client import RewardsServiceClient, RewardsServiceError

TIERS = [{"tier": "A", "rewardName": "5% off purchase", "points": 100}]
CUSTOMER = {
    "email": "customer01@gmail.com",
    "rewardPoints": 100,
    "rewardTier": "A",
    "rewardTierName": "5% off purchase",
    "nextRewardTier": "B",
    "nextRewardTierName": "10% off purchase",
    "nextRewardTierProgress": 0.5,
}


class RewardsViewGetTests(TestCase):

    @mock.patch.object(RewardsServiceClient, "get_all_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    def test_renders_tiers_and_all_customers(self, mock_get_rewards, mock_get_all):
        mock_get_rewards.return_value = TIERS
        mock_get_all.return_value = [CUSTOMER]

        response = self.client.get(reverse('rewards'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['rewards_data'], TIERS)
        self.assertEqual(response.context['customer_rewards_data'], [CUSTOMER])
        self.assertContains(response, "customer01@gmail.com")

    @mock.patch.object(RewardsServiceClient, "get_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    def test_email_filter_shows_single_customer(self, mock_get_rewards, mock_get_customer):
        mock_get_rewards.return_value = TIERS
        mock_get_customer.return_value = CUSTOMER

        response = self.client.get(reverse('rewards'), {"email": "customer01@gmail.com"})

        self.assertEqual(response.status_code, 200)
        mock_get_customer.assert_called_once_with("customer01@gmail.com")
        self.assertEqual(response.context['customer_rewards_data'], [CUSTOMER])

    @mock.patch.object(RewardsServiceClient, "get_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    def test_email_filter_not_found_shows_warning(self, mock_get_rewards, mock_get_customer):
        mock_get_rewards.return_value = TIERS
        mock_get_customer.return_value = None

        response = self.client.get(reverse('rewards'), {"email": "nobody@gmail.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['customer_rewards_data'], [])
        self.assertContains(response, "No rewards data found")

    @mock.patch.object(RewardsServiceClient, "get_all_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    def test_service_error_shows_error_message(self, mock_get_rewards, mock_get_all):
        mock_get_rewards.side_effect = RewardsServiceError("service is down")
        mock_get_all.return_value = []

        response = self.client.get(reverse('rewards'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Could not load reward tiers")


class RewardsViewPostTests(TestCase):

    @mock.patch.object(RewardsServiceClient, "get_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    @mock.patch.object(RewardsServiceClient, "submit_order")
    def test_add_order_success_redirects_with_message(
        self, mock_submit_order, mock_get_rewards, mock_get_customer
    ):
        mock_submit_order.return_value = CUSTOMER
        mock_get_rewards.return_value = TIERS
        mock_get_customer.return_value = CUSTOMER

        response = self.client.post(
            reverse('rewards'),
            {"email": "customer01@gmail.com", "order_total": "100.80"},
            follow=True,
        )

        self.assertRedirects(response, reverse('rewards') + "?email=customer01%40gmail.com")
        mock_submit_order.assert_called_once_with("customer01@gmail.com", 100.80)
        self.assertContains(response, "submitted successfully")

    def test_add_order_missing_fields_shows_error(self):
        response = self.client.post(
            reverse('rewards'), {"email": "", "order_total": ""}, follow=True
        )

        self.assertRedirects(response, reverse('rewards'))
        self.assertContains(response, "provide both an email address and an order total")

    def test_add_order_non_numeric_total_shows_error(self):
        response = self.client.post(
            reverse('rewards'),
            {"email": "customer01@gmail.com", "order_total": "abc"},
            follow=True,
        )

        self.assertContains(response, "Order total must be a number")

    @mock.patch.object(RewardsServiceClient, "get_customer_rewards")
    @mock.patch.object(RewardsServiceClient, "get_rewards")
    @mock.patch.object(RewardsServiceClient, "submit_order")
    def test_add_order_service_error_shows_error(
        self, mock_submit_order, mock_get_rewards, mock_get_customer
    ):
        mock_submit_order.side_effect = RewardsServiceError("orderTotal must be greater than 0")
        mock_get_rewards.return_value = TIERS
        mock_get_customer.return_value = None

        response = self.client.post(
            reverse('rewards'), {"email": "customer01@gmail.com", "order_total": "0"}, follow=True
        )

        self.assertContains(response, "Could not submit order")
