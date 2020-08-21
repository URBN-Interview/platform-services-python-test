import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from rewards.forms import AddOrder, Search

from django.shortcuts import redirect
import requests
from django.http import HttpResponseRedirect
import json

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.rewards_data =  rewards_service_client.get_rewards()
        self.customer_rewards = rewards_service_client.get_all_customers()


	#getting a single customer reward, all customers rewards, all rewards
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['rewards_data'] = self.rewards_data
        context['customer_rewards'] = self.customer_rewards
        # search_form = Search(request.GET)

        if request.method == "GET":
        	search_form = Search(request.GET)
        	#If the user inputs an email, return the specific customer  
        	if search_form.is_valid():
        		if search_form.cleaned_data['emailAddress']:
        			single_customer = self.rewards_service_client.get_customer(search_form.cleaned_data['emailAddress'])
        			context['single_customer'] = single_customer
        			#else if there is no input in the email field
        		else:
        			customer_rewards = self.rewards_service_client.get_all_customers()
        			context['customer_rewards'] = customer_rewards
	        else:
	        	context['search_customer_error'] = 'Please input a valid email address to search'
        
        return TemplateResponse(
            request,
            self.template_name,
            context
        )



    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)        
        if request.method == "POST":

            order_form = AddOrder(request.POST)
            if order_form.is_valid():
            	emailAddress = order_form.cleaned_data['emailAddress']
            	orderTotal = order_form.cleaned_data['orderTotal']
            	requests.post("http://rewardsservice:7050/order", data = { "emailAddress" : emailAddress, "orderTotal" : orderTotal })
            return HttpResponseRedirect("/rewards")
        return TemplateResponse(
            request,
            self.template_name,
            context
        )