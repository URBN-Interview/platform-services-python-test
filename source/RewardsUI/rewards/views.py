import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient, CustomerRewardsClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return TemplateResponse(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        email = ""
        amount = 0

        if request.POST.get("email_address") is not None:
            email = request.POST.get('email_address')
            amount = request.POST.get('amount')

        post_rewards = self.rewards_service_client.post_rewards(email, amount)
        context['message'] = post_rewards

        self.get(request, **kwargs)
        return TemplateResponse(request, self.template_name, context)
