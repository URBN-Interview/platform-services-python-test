import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from rewards.clients.customer_service_client import CustomerServiceClient

from .forms import orderDetail
from .forms import customerDetail


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient(), customer_service_client=CustomerServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
        self.customer_service_client = customer_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def getAllCustomers(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if (request.method == "GET"):
            customer_data = self.customer_service_client.getAllCustomers()
            context['customer_data'] = customer_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def getCustomer(self, request, *args, **kwargs):
        if(request.method == 'GET'):
            form = customerDetail(request.GET)
            if form.is_valid():
                emailAddress = form.cleaned_data['email']
                customer_data = self.customer_service_client.getCustomer(email)
        context['customer_data'] = customer_data

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if(request.method == 'POST'):
            form = orderDetail(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                total = form.cleaned_data['total']
                order_data = self.customer_service_client.postCustomer(
                    email, total)
            context['order_data'] = order_data

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
