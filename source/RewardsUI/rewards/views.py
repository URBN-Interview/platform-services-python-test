import json
import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.forms import OrderForm, UserRewardsForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        customer_data = self.rewards_service_client.get_all_customer_data()
        context['customer_data'] = customer_data

        form = OrderForm(request.GET)
        context['order_form'] = form

        user_rewards_form = UserRewardsForm(request.GET)
        context['user_rewards_form'] = user_rewards_form

        if user_rewards_form.is_valid():
            try:
                email = user_rewards_form.cleaned_data.get("email_filter")
                user_data = self.rewards_service_client.get_user_rewards(email)
                context['customer_data'] = user_data
            except json.decoder.JSONDecodeError:
                # returns error message is user not found
                messages.error(request, 'User not found')

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = OrderForm(request.POST)
        context['order_form'] = form

        if form.is_valid():
            email = form.cleaned_data.get("email")
            order_total = form.cleaned_data.get("order_total")
            self.rewards_service_client.post_calculate_rewards(email, order_total)
        return HttpResponseRedirect('/rewards/')

