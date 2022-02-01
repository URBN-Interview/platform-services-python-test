import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms import Form
from django.http import Http404

from rewards.clients.rewards_service_client import RewardsServiceClient

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    #HTML GET request handler
    def get(self, request, *args, **kwargs):
        #Get the context
        context = self.get_context_data(**kwargs)

        #Retreive the rewards table and customer table
        rewards_data = self.rewards_service_client.get_rewards()
        all_customers = self.rewards_service_client.all_customers()
        context['rewards_data'] = rewards_data
        context['all_customers'] = all_customers

        #Reload the HTML template
        return TemplateResponse(request, self.template_name, context)

    #HTML POST request handler
    def post(self, request, *args, **kwargs):
        #Get the context and keep the rewards table
        context = self.get_context_data(**kwargs)
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        #If the post request was sent by the add orders section
        if 'email' in request.POST:
            emailInput = request.POST.get('email')
            totalInput = request.POST.get('total')
            all_customers = self.rewards_service_client.insert_order(emailInput, totalInput)
            context['all_customers'] = all_customers

        #If the post request was sent by the find customer section
        elif 'user' in request.POST:
            searchResults = self.rewards_service_client.find_customer(request.POST.get('user'))
            context['all_customers'] = searchResults

        #Reload the page
        return render(self.request, self.template_name, context)
