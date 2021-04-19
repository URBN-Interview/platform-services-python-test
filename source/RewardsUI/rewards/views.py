import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from .forms import AddOrderForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_customers()
        context['add_order_form'] = AddOrderForm(request.POST)
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.method == 'POST':
            form = AddOrderForm(request.POST)
            email_address = form['email_address']
            order_total = form['order_total']
            add_order_data = self.rewards_service_client.add_order(email_address, order_total)
            context['add_order_data'] = add_order_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
