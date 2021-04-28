import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customers_service_client import CustomersServiceClient

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), customers_service_client=CustomersServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customers_service_client = customers_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        rewards_data = self.rewards_service_client.get_rewards()
        customer_data = self.customers_service_client.get_all_customers()
        context['rewards_data'] = rewards_data
        context['customer_data'] = customer_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )