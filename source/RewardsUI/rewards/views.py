import logging

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.forms import OrderForm, UserForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        users_data = self.rewards_service_client.get_all_users()
        context['users_data'] = users_data

        user_form = UserForm(request.GET)
        context['single_user_data'] = user_form

        if user_form.is_valid():
            email_address = user_form.cleaned_data['email_address']
            user_data = self.rewards_service_client.get_user_reward(email_address)
            context['users_data'] = [user_data]

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_form = OrderForm(request.POST)
        context['order_form'] = order_form
        if order_form.is_valid():
            email_address = order_form.cleaned_data['email_address']
            order_total = order_form.cleaned_data['order_total']
            self.rewards_service_client.add_order(email_address, order_total)

        return HttpResponseRedirect("/rewards")
