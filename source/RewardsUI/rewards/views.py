import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__),
                 rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        """Storing these methods as class variables because I will be using them more than once."""
        self.rewards_data = rewards_service_client.get_rewards()
        self.all_rewards_data = rewards_service_client.get_all_rewards()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rewards_data'] = self.rewards_data
        context['all_rewards_data'] = self.all_rewards_data
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    """Setting up a post method that uses the search_rewards_data_url endpoint IF the value of the form button is "Search", but otherwise
        uses the send_order_data_url url.
    """

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.POST['action'] == 'Search':
            searchEmail = request.POST.get("searchEmailAddress")
            all_rewards_data = self.rewards_service_client.search_rewards_data(
                searchEmail)
            context['rewards_data'] = self.rewards_data
            context['all_rewards_data'] = all_rewards_data
            return TemplateResponse(request, self.template_name, context)
        else:
            email = request.POST.get("emailAddress")
            total = request.POST.get("orderTotal")
            get_data = self.rewards_service_client.send_order_data(
                email, total)
            context['rewards_data'] = self.rewards_data
            return TemplateResponse(
                request,
                self.template_name, context
            )
