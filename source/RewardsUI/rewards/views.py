import logging
import re

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import AllCustomersRequest, CustomerRequest, OrderRequest, RewardsRequest
from .forms import EmailForm, OrderForm

class RewardsView(TemplateView):
    template_name = 'index.html'
    email_regrex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        inputError = ''

        try:
            rewards_data = RewardsRequest().request()
            customers_data = AllCustomersRequest().request()

            if request.method == 'GET':
                form = EmailForm(request.GET)
                if form.is_valid():
                    email = form.cleaned_data['email']
                    emailValidate = re.search(self.email_regrex , email)

                    if(email):
                        if(not emailValidate):
                            inputError = 'Invalid email'
                        else:
                            customers_data = CustomerRequest().request({'email': email})

            context['rewards_data'] = rewards_data
            context['customers_data'] = customers_data
            context['customer_input_error'] = inputError

        except:
            context['error'] = True

        finally:
            return TemplateResponse(
                    request,
                    self.template_name,
                    context
                )


    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        inputError = ''
        
        try:
            if request.method == 'POST':
                form = OrderForm(request.POST)
                print(form.is_valid())
                if form.is_valid():
                    email = form.cleaned_data['order_email']
                    orderTotal = '%.2f' % float(form.cleaned_data['order_total'])
                    emailValidate = re.search(self.email_regrex , email)
                    if(not emailValidate):
                        inputError = 'Invalid email'
                    else:
                        order = OrderRequest().request({'email': email, 'orderTotal': orderTotal})

            customers_data = AllCustomersRequest().request()
            rewards_data = RewardsRequest().request()
            
            context['order_input_error'] = inputError
            context['rewards_data'] = rewards_data
            context['customers_data'] = customers_data

        except:
            context['error'] = True

        finally:
            return TemplateResponse(
                request,
                self.template_name,
                context
            )
        
