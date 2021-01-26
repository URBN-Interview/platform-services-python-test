import logging

from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient


class CustomerRewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), customer_rewards_client=RewardsServiceClient()):
        self.logger = logger
        self.customer_rewards_client = customer_rewards_client

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        customer_email = request.POST.get("customer_email")
        customer_data = self.customer_rewards_client.get_customers(customer_email)
        context['customer_data'] = customer_data

        return TemplateResponse(request, self.template_name, context)
