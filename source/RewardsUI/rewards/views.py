import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render

from rewards.clients.rewards_service_client import RewardsServiceClient

from .forms import CustomerOrder

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    # Customer Order form handler
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context['form'].is_valid():
            form = context['form']
            user_email = form.cleaned_data['email']
            user_total = form.cleaned_data['total']

            # send to API
            self.rewards_service_client.customer_order({
                "email": user_email,
                "total": user_total
            })

            rewards_data = self.rewards_service_client.get_rewards()
            context['rewards_data'] = rewards_data
            print('test')
        
        return super(TemplateView, self).render_to_response(context)
    
    # expansion on get_context_data
    # used to add form models to the context of the TemplateView
    # note - check if CSRF needs to be enabled
    def get_context_data(self, **kwargs):
        context = super(RewardsView, self).get_context_data(**kwargs)
        form = CustomerOrder(self.request.POST or None)
        context['form'] = form
        return context 