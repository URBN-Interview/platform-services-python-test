import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customer_service_client import CustomerServiceClient

from .forms import CustomerOrder, CustomerEmailSearch

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(
            self, 
            logger=logging.getLogger(__name__), 
            rewards_service_client=RewardsServiceClient(),
            customer_service_client=CustomerServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customer_service_client = customer_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    # form handler
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['customer_order_form'].is_valid():
            form = context['customer_order_form']
            user_email = form.cleaned_data['email']
            user_total = form.cleaned_data['total']

            # send to API
            resp = self.rewards_service_client.customer_order({
                'email': user_email,
                'total': user_total
            })

            if not resp.success:
                context['customer_order_error'] = "\
                    Error adding customer! Customer not added."
        else:
            customer_order_form = CustomerOrder(self.request.POST or None)
            context['customer_order_form'] = customer_order_form

        if context['email_search_form'].is_valid():
            form = context['email_search_form']
            email = form.cleaned_data['search_email']

            resp = self.customer_service_client.get_customer(email)
            context['customers_data'] = []
            if len(resp['customer']) > 0:
                context['customers_data'].append(resp.customer)
                
        else:
            email_search_form = CustomerEmailSearch(self.request.POST or None)
            context['email_search_form'] = email_search_form
        
        return super(TemplateView, self).render_to_response(context)
    
    # get_context_data
    # used to add form models to the context of the TemplateView
    # used to add static context data needed for template display
    # note - check if CSRF needs to be enabled
    def get_context_data(self, **kwargs):
        context = super(RewardsView, self).get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data['rewards']

        # add in get all customers with reward data
        customers_data = self.customer_service_client.get_customers()
        context['customers_data'] = customers_data['customers']

        context['selected_customer'] = None
        context['customer_order_error'] = None
        
        customer_order_form = CustomerOrder(self.request.POST or None)
        context['customer_order_form'] = customer_order_form

        email_search_form = CustomerEmailSearch(self.request.POST or None)
        context['email_search_form'] = email_search_form

        return context 