import logging

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

from django.shortcuts import render

from .forms import OrderForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        all_customers_data = self.rewards_service_client.get_all_customers_data()
        context['all_customers_data'] = all_customers_data

        print("getter")
        print(request)

        
        form=OrderForm()
        context["form"] = form
        
        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        print("before form")
        form = OrderForm(request.POST)
        print("after form")
        if form.is_valid():
            print(form)
            email = form.cleaned_data['user_email']
            order = form.cleaned_data['user_order']

            post_status = self.rewards_service_client.send_customer_data(email, order)
            context["order_status"] = "test"

        return HttpResponseRedirect('/rewards/', context)



