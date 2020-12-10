import logging

from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.rewards_service_client import RewardMembersClient
from rewards.clients.rewards_service_client import OrderClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), members_service_client=RewardMembersClient(), order_service_client=OrderClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.members_service_client = members_service_client
        self.order_service_client = order_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        members_data = self.members_service_client.get_members()
        context['members_data'] = members_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.POST.get("email"):
            email = request.POST.get("email")
            purchase = request.POST.get("purchase")

            json = {"email": email, "purchase": purchase}

            print(json)

            self.order_service_client.post_order(json)

            rewards_data = self.rewards_service_client.get_rewards()
            context['rewards_data'] = rewards_data

            members_data = self.members_service_client.get_members()
            context['members_data'] = members_data

        elif request.POST.get("search"):
            email = request.POST.get("search")



        return render(
            request,
            self.template_name,
            context
        )


