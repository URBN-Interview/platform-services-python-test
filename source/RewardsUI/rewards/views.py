import logging, requests
from requests.structures import CaseInsensitiveDict
from rewards.services import get_all_user_rewards
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
        context['add_points_endpoint'] = "http://localhost:7050/endpoint_one"
        try:
            r = requests.get("http://localhost:7050/endpoint_three")
        except Exception as e:
            print("the exception is {}".format(e))
            

        return TemplateResponse(
            request,
            self.template_name,
            context
        )