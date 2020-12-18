import logging
import json

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customers_client import CustomersClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), customers_client=CustomersClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customers_client = customers_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.customers_client.get_customers()
        for customer in customers_data:
            customer['nextRewardTierProgressPercent'] = customer['nextRewardTierProgress'] * 100
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        filterEmail = request.POST.get("filter-email")
        orderEmail = request.POST.get("order-email")
        orderTotal = request.POST.get("order-total")

        customers_data = {}
        if filterEmail:
            customers_data = [self.customers_client.get_customer(filterEmail)]
        else:
            if orderEmail and orderTotal:
                self.customers_client.post_order(orderEmail, orderTotal)
            customers_data = self.customers_client.get_customers()

        rewards_data = self.rewards_service_client.get_rewards()
        for customer in customers_data:
            print(customer)
            customer['nextRewardTierProgressPercent'] = customer['nextRewardTierProgress'] * 100
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
