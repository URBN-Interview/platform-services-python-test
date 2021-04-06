import logging

from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from .forms import EmailFilterForm, PostOrderForm

from rewards.clients.rewards_service_client import RewardsServiceClient


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        #get context data for inital render 
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        customers_data = self.rewards_service_client.get_customers()
        context['customers_data'] = customers_data

        #declare forms and add to view context
        filter_form = EmailFilterForm(request.GET)
        context["filter_form"] = filter_form
        order_form = PostOrderForm(request.GET)
        context['order_form'] = order_form

        #check if user input from form is valid
        #requests desired email information then resets context data
        if filter_form.is_valid():
            email = filter_form.cleaned_data.get("email_filter")
            single_customers_data = self.rewards_service_client.get_single_customer(email)
            context['customers_data'] = single_customers_data
        

        return TemplateResponse(
            request,
            self.template_name,
            context
        )


    #accepts new order information and posts to database then refreshes view
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        order_form = PostOrderForm(request.POST)
        context['order_form'] = order_form

        if request.method == "POST":
            if order_form.is_valid():
                email = order_form.cleaned_data.get("email")
                orderTotal = order_form.cleaned_data.get("total")
                order = self.rewards_service_client.post_customer(email, orderTotal)
        
        return HttpResponseRedirect('/rewards/')

