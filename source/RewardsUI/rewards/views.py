import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import EmailForm, OrderForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customer_data = self.rewards_service_client.get_customers()

        context['rewards_data'] = rewards_data
        context['customer_data'] = customer_data
        if request.method == 'GET':
            form = EmailForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data['email'])

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        customer_data = self.rewards_service_client.get_customers()

        print(customer_data)

        context['rewards_data'] = rewards_data
        context['customer_data'] = customer_data

        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
            
        return TemplateResponse(
            request,
            self.template_name,
            context
        )
        
