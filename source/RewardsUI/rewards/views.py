import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        print("request obj", request.GET)
        if "email" in request.GET:
            customers_data = self.rewards_service_client.get_single_customer()
            context['customers_data'] = customers_data
        else:
            customers_data = self.rewards_service_client.get_customers()
            context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    #def put(self, request, *args, **kwargs):
