import logging
import json

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .form import EmailForm, OrderForm	
from django.http import HttpResponseRedirect


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        # get_rewards and get_customers data from client
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()	
        customers_data = self.rewards_service_client.get_customers()	
        # context to feed index.html	
        context['rewards_data'] = rewards_data	
        context['customers_data'] = customers_data	

        if request.method == "GET":	
            email_form = EmailForm(request.GET)	
            if email_form.is_valid():	
                email = email_form.cleaned_data['email']	
                customers_data = self.rewards_service_client.get_customer(email)	
                context['customers_data'] = customers_data	
            else:	
                context['input_error'] ="Something went wrong, please try again"

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):	
        context = self.get_context_data(**kwargs)	

        if request.method == "POST":	
            order_form = OrderForm(request.POST)	
            if order_form.is_valid():	
                email = order_form.cleaned_data['order_email']	
                orderTotal = order_form.cleaned_data['order_total']
                order = request.POST['order_email']	

            # order= self.rewards_service_client.get_order(email, orderTotal)	
                # order.save()	

            else:	
                context['input_error'] ="Something went wrong, please try again"	
            return HttpResponseRedirect("/rewards")	
        customers_data = self.rewards_service_client.get_customers()
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        context['customers_data'] = customers_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
