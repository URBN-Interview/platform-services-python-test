import logging
import json

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.endpoint1_client import Endpoint1Client
from rewards.clients.endpoint2_client import Endpoint2Client
from rewards.clients.endpoint3_client import Endpoint3Client

# get all rewards, get all users
class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), endpoint3_client=Endpoint3Client()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.endpoint3_client = endpoint3_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        user_data = self.endpoint3_client.get_all_users()

        context['rewards_data'] = rewards_data
        context['user_data'] = user_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
# add order
class AddOrderView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), endpoint1_client=Endpoint1Client()):
        self.logger = logger
        self.endpoint1_client = endpoint1_client

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST["email"]
            order_total = request.POST["order_total"]
        
            self.endpoint1_client.add_order(email, order_total)

            return HttpResponseRedirect(reverse("rewards"))
        
# search for user
class SearchUserView(TemplateView):
    template_name = 'index.html'
    
    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), endpoint2_client=Endpoint2Client(), endpoint3_client=Endpoint3Client(), rewards_data=None, user_data=None):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.endpoint2_client = endpoint2_client
        self.endpoint3_client = endpoint3_client
        self.rewards_data = self.rewards_service_client.get_rewards()
        self.user_data = self.endpoint3_client.get_all_users()


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        user_data = self.endpoint3_client.get_all_users()

        context['rewards_data'] = rewards_data
        context['user_data'] = user_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            email = request.POST["email"]

            self.endpoint2_client.search_user(email)

            # user_data = self.endpoint3_client.get_all_users()
            context['rewards_data'] = self.rewards_data
            context['user_data'] = self.user_data

            # for user in user_data:
            #     if user['email'] != email

            # return HttpResponseRedirect(reverse("rewards"))

            return TemplateResponse(
            request,
            self.template_name,
            context
        )


