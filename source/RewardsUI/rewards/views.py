import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.all_user_info_service_client import AllUserInfoServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(),
                 all_user_info_service_client=AllUserInfoServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.all_user_info_service_client = all_user_info_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        all_user_data = self.all_user_info_service_client.get_all_user_info()
        context['all_user_data'] = all_user_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
