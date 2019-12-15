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

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email_address = request.POST.get("email_address", None)
        order_total = request.POST.get("order_total", None)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        order_data = self.rewards_service_client.add_order(email_address, order_total)
        context.update(order_data)

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
