import logging
import requests
import json


from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from .forms import AddOrderForm
from rewards.forms import QueryUser


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

        all_customers = self.rewards_service_client.get_all()
        context['all_customers'] = all_customers

        # one_customer = self.rewards_service_client.get_user()
        # context['one_customer'] = one_customer

        add_order_form = AddOrderForm()
        context['add_order_form'] = add_order_form

        

        # form = QueryUser(request.GET)
        

        # if form.is_valid():
        #     if(form.cleaned_data['emailAddress'] != ""):
        #         email = get_user.cleaned_data['emailAddress']
        #         response = requests.get("http://rewardsservice:7050/get" + email)
        #         context['get_user'].append(response.json())
                
        # else:
        #     all_customers = self.rewards_service_client.get_all()
        #     context['all_customers'] = all_customers

      

        return TemplateResponse(
            request,
            self.template_name,
            context
          
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        add_order_form = AddOrderForm(request.POST)
        context['add_order_form'] = add_order_form
        if add_order_form.is_valid():
            email = add_order_form.cleaned_data['emailAddress']
            order = add_order_form.cleaned_data['orderTotal']
            requests.post("http://rewardsservice:7050/set", data = { "emailAddress" : email, "orderTotal" : order })
        return HttpResponseRedirect("/rewards") 
 
