import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView, View
from django.http import HttpResponseRedirect, HttpResponse
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
    
    # form handler for email search
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        action = request.POST["action"]
        if action == "add_orders":
            customer_order = CustomerOrder(self.request.POST)

            if customer_order.is_valid():
                form = customer_order
                user_email = form.cleaned_data['email']
                user_total = form.cleaned_data['total']

                # send to API
                resp = self.rewards_service_client.add_order({
                    'email': user_email,
                    'total': user_total
                })

                if not resp['success']:
                    context['customer_order_error'] = "\
                        Error adding customer! Customer not added."
                else:
                    return HttpResponseRedirect("/rewards/")
        elif action == "search":
            order_search = CustomerEmailSearch(request.POST)
            if order_search.is_valid():
                form = order_search
                email = form.cleaned_data['search_email']

                resp = self.customer_service_client.get_customer(email)
                context['customers_data'] = []
                if len(resp['customer']) > 0:
                    context['customers_data'] = resp['customer']
                    
            else:
                email_search_form = CustomerEmailSearch()
                order_search = email_search_form
        elif action == "reset":
             # add in get all customers with reward data
            customers_data = self.customer_service_client.get_customers()
            context['customers_data'] = customers_data['customers']
        
        return super(TemplateView, self).render_to_response(context)
    
    # get_context_data
    # used to add form models to the context of the TemplateView
    # used to add static context data needed for template display
    def get_context_data(self, **kwargs):
        context = super(RewardsView, self).get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data['rewards']

        # add in get all customers with reward data
        customers_data = self.customer_service_client.get_customers()
        context['customers_data'] = customers_data['customers']

        context['selected_customer'] = None
        context['customer_order_error'] = None
        
        customer_order_form = CustomerOrder()
        context['customer_order_form'] = customer_order_form

        email_search_form = CustomerEmailSearch()
        context['email_search_form'] = email_search_form

        return context 