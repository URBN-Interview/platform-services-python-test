import logging
from urllib.parse import quote_plus

from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient, RewardsServiceError


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        email_filter = request.GET.get('email', '').strip()
        context['email_filter'] = email_filter

        try:
            context['rewards_data'] = self.rewards_service_client.get_rewards()
        except RewardsServiceError as e:
            self.logger.exception("Failed to load reward tiers")
            messages.error(request, "Could not load reward tiers: {}".format(e))
            context['rewards_data'] = []

        try:
            if email_filter:
                customer = self.rewards_service_client.get_customer_rewards(email_filter)
                context['customer_rewards_data'] = [customer] if customer else []
                if not customer:
                    messages.warning(request, "No rewards data found for '{}'.".format(email_filter))
            else:
                context['customer_rewards_data'] = self.rewards_service_client.get_all_customer_rewards()
        except RewardsServiceError as e:
            self.logger.exception("Failed to load customer rewards")
            messages.error(request, "Could not load customer rewards: {}".format(e))
            context['customer_rewards_data'] = []

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '').strip()
        order_total = request.POST.get('order_total', '').strip()

        if not email or not order_total:
            messages.error(request, "Please provide both an email address and an order total.")
            return self._redirect_to_rewards(email)

        try:
            order_total = float(order_total)
        except ValueError:
            messages.error(request, "Order total must be a number.")
            return self._redirect_to_rewards(email)

        try:
            self.rewards_service_client.submit_order(email, order_total)
            messages.success(request, "Order for {} submitted successfully.".format(email))
        except RewardsServiceError as e:
            self.logger.exception("Failed to submit order")
            messages.error(request, "Could not submit order: {}".format(e))

        return self._redirect_to_rewards(email)

    def _redirect_to_rewards(self, email_filter):
        url = reverse('rewards')
        if email_filter:
            url = "{}?email={}".format(url, quote_plus(email_filter))
        return redirect(url)
