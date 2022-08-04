import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages

from .orders_form import OrdersForm
from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        user_rewards = self.rewards_service_client.get_user_rewards()
        context['rewards_data'] = rewards_data
        context['user_rewards'] = user_rewards
        context['form'] = OrdersForm()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request):
        form = OrdersForm(request.POST)
        if form.is_valid():
            response = self.rewards_service_client.submit_order(request.POST)
            if response.status_code != 200:
                messages.add_message(request, messages.ERROR, "There was something wrong with your input: " + response.reason)
            return HttpResponseRedirect('/rewards/')
