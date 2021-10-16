import logging
import json
from django.core.exceptions import ValidationError
from django.shortcuts import render

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient
from .forms import CustomerOrderForm, CustomerRewardForm

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def post(self, request, *args, **kwargs):        
        context = self.get_context_data(**kwargs)
        
        all_customer_rewards = self.rewards_service_client.get_all_customer_rewards()
        context['all_customer_rewards'] = all_customer_rewards
        customer_order_form = CustomerOrderForm()   
        customer_reward_form = CustomerRewardForm() 

        if (request.method == 'POST'):
            #First form to submit order to add rewards
            if 'Submit Order Form' in request.POST:     
                print("Submit Order Form")            
                customer_order_form = CustomerOrderForm(request.POST)    
                if customer_order_form.is_valid():                
                    customer_email_address = customer_order_form.cleaned_data.get("customer_email_address")
                    customer_order = customer_order_form.cleaned_data.get("customer_order") 
                    print("customer_order ", customer_order)               
                    post_response = self.rewards_service_client.post_customer_order(customer_email_address, customer_order)
                    response_text = json.loads(post_response.text)
                    response_status = post_response.status_code
                    all_customer_rewards = self.rewards_service_client.get_all_customer_rewards()
                    if (response_status == 400):
                        print("Raising ValidationError")  
                        raise ValidationError(response_text['message'])
                    else:
                        customer_order_form = CustomerOrderForm()                
                else:
                    print("data is invalid", customer_order_form.is_valid())                              
            
            #Second form to find the reward for email
            elif 'Search Form' in request.POST:    
                print("Search Form") 
                customer_reward_form = CustomerRewardForm(request.POST)   
                if customer_reward_form.is_valid():   
                    customer_email_address = customer_reward_form.cleaned_data.get("customer_email_address")
                    post_response = self.rewards_service_client.post_customer_reward(customer_email_address)
                    response_text = json.loads(post_response.text)
                    
                    all_customer_rewards = response_text
                    
                    response_status = post_response.status_code
                    if (response_status == 400):
                        print("Raising ValidationError")  
                        raise ValidationError(response_text['message'])
                    else:
                        customer_reward_form = CustomerRewardForm()     
            else:       
                customer_order_form = CustomerOrderForm()   
                customer_reward_form = CustomerRewardForm() 
        
        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data
        return render(request, 'index.html', {'customer_reward_form':customer_reward_form, 'customer_order_form': customer_order_form,"all_customer_rewards":all_customer_rewards , "rewards_data":rewards_data})

    def get(self, request, *args, **kwargs):         
        context = self.get_context_data(**kwargs)

        rewards_data = self.rewards_service_client.get_rewards()
        context['rewards_data'] = rewards_data

        all_customer_rewards = self.rewards_service_client.get_all_customer_rewards()
        context['all_customer_rewards'] = all_customer_rewards

        if (request.method == 'POST'):
            customer_order_form = CustomerOrderForm(request.POST)        
            customer_reward_form = CustomerRewardForm(request.POST)
        else: 
            customer_order_form = CustomerOrderForm()
            customer_reward_form = CustomerRewardForm()

        context['customer_order_form'] = customer_order_form
        context['customer_reward_form'] = customer_reward_form

        return TemplateResponse(
            request,
            self.template_name,
            context
        )
