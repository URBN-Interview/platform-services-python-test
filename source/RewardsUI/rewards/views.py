import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.rewards_data = []

    def get_rewards_data(self):
        if not self.rewards_data:
            self.rewards_data = self.rewards_service_client.get_rewards()
        return self.rewards_data

    def get(self, request, *args, **kwargs):
        email_address = request.GET.get("email", "")
        context = self.get_context_data(**kwargs)

        rewards_data = self.get_rewards_data()
        users_data = self.rewards_service_client.get_users(email_address=email_address)
        context['rewards_data'] = rewards_data
        context['users_data'] = users_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        email_address = request.POST.get("email_address", "")
        order_total = request.POST.get("order_total", 0)
        data = self.rewards_service_client.add_rewards(email_address=email_address, order_total=order_total)
        context = self.get_context_data(**kwargs)
        rewards_data = self.get_rewards_data()
        users_data = self.rewards_service_client.get_users()
        context['rewards_data'] = rewards_data
        context['users_data'] = users_data
        context['response_data'] = data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
