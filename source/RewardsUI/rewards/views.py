import logging
from django.http import response

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import CustomerOrder
from .forms import GetCustomer

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        if(not rewards_data):
            context["rewards_not_found"] = "No rewards tier defined!!"

        
        # Get customer rewards data
        customer_rewards_data = self.rewards_service_client.get_all_customer_rewards()
        context['customer_rewards_data'] = customer_rewards_data
        if(not customer_rewards_data):
            context["customers_not_found"] = "customers data not found!!"

        context['search_reward_form'] = GetCustomer()
        context['add_customer_rewards'] = CustomerOrder()

        if(request.method == 'GET'):
            form = GetCustomer(request.GET)
            if(form.is_valid()):
                if(form.cleaned_data["email"]):
                    email = form.cleaned_data["email"]
                    customer_rewards = self.rewards_service_client.get_customer_rewards(email)
                    context["customer_rewards_data"] = customer_rewards
                    # Error checks to see if email is found or not
                    if(not customer_rewards):
                        context["customer_email_not_found"] = "No data found, please check the email provided and try again!!"

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if(request.method == 'POST'):
            form = CustomerOrder(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                total = form.cleaned_data['orderTotal']
                order_data = self.rewards_service_client.add_customer_rewards(
                    email, total)
            
            context["rewards_added"] = "Customer reward points added!!"

            rewards_data = self.rewards_service_client.get_rewards()
            context['rewards_data'] = rewards_data
            
            # Get customer rewards data
            customer_rewards_data = self.rewards_service_client.get_all_customer_rewards()
            context['customer_rewards_data'] = customer_rewards_data

            context['search_reward_form'] = GetCustomer()
            context['add_customer_rewards'] = CustomerOrder()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )