import logging
import requests
import time

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient
from django.views.decorators.csrf import csrf_exempt
import socket
import urllib

class RewardsView(TemplateView):
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
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        submit_data = self.rewards_service_client.submit_order(email, amount)
        print(submit_data)

        context['order_message'] = "Order of amount " + amount + " by " + email + " successfully sent!"

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return render(request, self.template_name, context)