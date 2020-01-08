import logging
import sys

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from django.http import HttpResponseRedirect


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        all_customers_data = self.rewards_service_client.get_all_customers()
        context['all_customers_data'] = all_customers_data

        # if 'submit_search' in request.POST:
        single_customer_data = self.rewards_service_client.get_single_customer()
        context['single_customer_data'] = single_customer_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
