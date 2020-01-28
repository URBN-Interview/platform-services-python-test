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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        all_rewards_data = self.rewards_service_client.get_all_rewards()
        context['rewards_data'] = rewards_data
        context['all_rewards_data'] = all_rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    # """Setting up a post method that uses the send_order_data url IF the form input value equals "Search", but otherwise
    #     uses the search_rewards_data url.
    # """
    # def post(self, request, **kwargs):
    #     if request.POST['action'] == 'Search':
    #         context = self.get_context_data(**kwargs)
    #         searchEmail = request.POST.get("searchEmailAddress")
    #         searchRewards = self.rewards_service_client.search_rewards_data(
    #             searchEmail)
    #         context['searchRewards'] = searchRewards
    #         return TemplateResponse(request, self.template_name, context)
    #     else:
    #         email = request.POST.get("emailAddress")
    #         total = request.POST.get("orderTotal")
    #         context = self.get_context_data(**kwargs)
    #         rewards_data = self.rewards_service_client.get_rewards()
    #         context['rewards_data'] = rewards_data
    #         get_data = self.rewards_service_client.send_order_data(
    #             email, total)
    #         return TemplateResponse(
    #             request,
    #             self.template_name, context
    #         )
