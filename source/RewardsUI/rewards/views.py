import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render

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

        return TemplateResponse(request, self.template_name, context)

class ClientRewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    #def get(self, request, *args, **kwargs):
    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print('here we go')
        reward_data = self.rewards_service_client.get_reward('b@b.com')
        context['reward_data'] = reward_data

        #return TemplateResponse(request, self.template_name, context)
        return render(request, template_name, context)
