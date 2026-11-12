# Views for the Rewards Dashboard. They fetch data from the RewardsService API
# through RewardsServiceClient and render it with the index.html template.

import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    """Renders the Rewards Dashboard page (index.html).

    GET: fetches the reward tiers from RewardsService and passes them to the
    template as `rewards_data`. The logger and API client can be injected,
    which makes the view easy to unit-test with a fake client.
    """

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
