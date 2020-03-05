import logging
import re

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import EmailForm, OrderForm

class RewardsView(TemplateView):
    template_name = 'index.html'
    email_regrex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        error = ''
        rewards_data = self.rewards_service_client.get_rewards()
        customers_data = self.rewards_service_client.get_all_customers()

        if request.method == 'GET':
            form = EmailForm(request.GET)
            if form.is_valid():
                email = form.cleaned_data['email']
                emailValidate = re.search(self.email_regrex , email)

                if(email):
                    print(emailValidate)
                    if(not emailValidate):
                        error = 'Invalid email input'
                    else:
                        customers_data = self.rewards_service_client.get_customer(email)
        
        if(type(customers_data) != list and customers_data.error):
            error = customers_data.context
        else:
            context['customers_data'] = customers_data

        context['customer_error'] = error
        context['rewards_data'] = rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        error = ''

        if request.method == 'POST':
            form = OrderForm(request.POST)
            print(form.is_valid())
            if form.is_valid():
                email = form.cleaned_data['order_email']
                orderTotal = '%.2f' % float(form.cleaned_data['order_total'])
                emailValidate = re.search(self.email_regrex , email)
                if(not emailValidate):
                    error = 'Invalid email input'
                else:
                    self.rewards_service_client.save_order(email, orderTotal)

        customers_data = self.rewards_service_client.get_all_customers()

        if(type(customers_data) != list and customers_data.error):
            error = customers_data.context
        else:
            context['customers_data'] = customers_data
        
        context['order_error'] = error
        context['rewards_data'] = rewards_data
        
        return TemplateResponse(
            request,
            self.template_name,
            context
        )
        
