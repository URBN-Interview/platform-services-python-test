import logging

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient, RewardsServiceError
from rewards.forms import CustomerSearchForm, OrderForm

logger = logging.getLogger(__name__)


class RewardsView(TemplateView):
    template_name = 'index.html'
    rewards_service_client = RewardsServiceClient(settings.REWARDS_SERVICE_URL)

    def get(self, request, *args, **kwargs):
        return self.render(request, order_form=OrderForm())

    def post(self, request, *args, **kwargs):
        """Submit an order, then redirect back (Post/Redirect/Get) to show the result."""
        order_form = OrderForm(request.POST)
        if not order_form.is_valid():
            return self.render(request, order_form=order_form, status=400)

        email = order_form.cleaned_data['email']
        try:
            rewards = self.rewards_service_client.add_order(
                email, str(order_form.cleaned_data['order_total']),
            )
        except RewardsServiceError as e:
            order_form.add_error(None, e.message)
            is_client_error = e.status_code is not None and 400 <= e.status_code < 500
            return self.render(request, order_form=order_form, status=400 if is_client_error else 502)

        messages.success(request, "Order added for {}. They now have {} points{}.".format(
            rewards['email'],
            rewards['points'],
            " (tier {})".format(rewards['tier']) if rewards.get('tier') else "",
        ))
        return redirect('rewards')

    def render(self, request, order_form, status=200):
        context = self.get_context_data()
        context['order_form'] = order_form
        context['search_form'] = search_form = CustomerSearchForm(request.GET or None)
        context['errors'] = errors = []

        try:
            context['rewards_data'] = self.rewards_service_client.get_rewards()
        except RewardsServiceError as e:
            context['rewards_data'] = []
            errors.append("Could not load reward tiers: {}".format(e.message))

        context['customers'] = []
        try:
            if search_form.is_bound and search_form.is_valid() and search_form.cleaned_data['email']:
                context['search_email'] = email = search_form.cleaned_data['email'].lower()
                customer = self.rewards_service_client.get_customer(email)
                context['customers'] = [customer] if customer else []
            else:
                context['customers'] = self.rewards_service_client.get_customers()
        except RewardsServiceError as e:
            errors.append("Could not load customer rewards: {}".format(e.message))

        return TemplateResponse(request, self.template_name, context, status=status)
