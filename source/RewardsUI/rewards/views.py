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
import json

def stringifyPercent(val):
    if val == 'N/A':
        # don't need % mark on N/A string
        string = val
        pass
    else:
        string = str(round(val * 100, 1)) + '%'
    
    return string

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        users_data = self.rewards_service_client.get_allusers()

        for user in users_data:
            user['nextProgress'] = stringifyPercent(user['nextProgress'])

        context['users_data'] = users_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if 'amount' in request.POST: # amount key only in submit form
            email = request.POST.get('email')
            amount = request.POST.get('amount')

            submit_data = self.rewards_service_client.submit_order(email, amount)

            context['order_message'] = "Order of amount " + amount + " by " + email + " successfully sent!"
            users_data = self.rewards_service_client.get_allusers()
        else:
            email = request.POST.get('email')
            user_data = self.rewards_service_client.get_user(email)
            user_data['nextProgress'] = stringifyPercent(user_data['nextProgress'])
            users_data = [] # users_data context must be a list
            users_data.append(user_data)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        for user in users_data:
            user['nextProgress'] = stringifyPercent(user['nextProgress'])
        context['users_data'] = users_data

        return render(request, self.template_name, context)
