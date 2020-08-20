import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from .forms import AddOrder
from rewards.forms import Search
from django.shortcuts import redirect
import json
from django.http import HttpResponseRedirect

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
        all_customers = self.rewards_service_client.get_all_customers()
        context['all_customers'] = all_customers
        search_form = Search(request.GET)
        context['search_form'] = search_form
        if search_form.is_valid():
            email_address = search_form.cleaned_data['email_address']
            requests.get("http://rewardsservice:7050/customer", data = { "email_address" : email_address })

        add_order_form = AddOrder()
        context['add_order_form'] = add_order_form
        search_form = Search()
        context['search_form'] = search_form


        return TemplateResponse(
            request,
            self.template_name,
            context
        ) 


    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)


        add_order_form = AddOrder(request.POST)
        context['add_order_form'] = add_order_form
        if add_order_form.is_valid():
            email_address = add_order_form.cleaned_data['email_address']
            order_total = add_order_form.cleaned_data['order_total']
            requests.post("http://rewardsservice:7050/customer", data = { "emailAddress" : email_address, "orderTotal" : order_total })
        return HttpResponseRedirect("/rewards")


        return TemplateResponse(
            request,
            self.template_name,
            context
        )