import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

#imports for redirect and render
from django.shortcuts import redirect, render

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request):
        endpoint = self.request.path
        #testing:   print(endpoint)
        ### Get rewards a user can earn ###
        rewards_data = self.rewards_service_client.get_rewards() 
        all_customers_rewards_data = self.rewards_service_client.get_all_customers_rewards()
        return TemplateResponse(
            request,
            self.template_name,
            {'customer_rewards_data': all_customers_rewards_data, 'rewards_data': rewards_data }
        )

class CustomerRewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
    def get(self, request):
        endpoint = self.request.path

        email = request.GET.get('email')
        #testing:   print(email)

        if email:
            #try:
                customer_rewards_data = self.rewards_service_client.get_customer_rewards(email)
                print(endpoint)
                print(customer_rewards_data)
                ### Get rewards a user can earn ###
                rewards_data = self.rewards_service_client.get_rewards() 
                #if rewards_data.status_code == 200:
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'customer_rewards_data': customer_rewards_data,'rewards_data': rewards_data }
                )
        else:
            all_customers_rewards_data = self.rewards_service_client.get_all_customers_rewards()
            print(endpoint)
            print("ALL_Customers")
            ### Get rewards a user can earn ###2
            rewards_data = self.rewards_service_client.get_rewards() 
            return TemplateResponse(
                request,
                self.template_name,
                {'customer_rewards_data': all_customers_rewards_data, 'rewards_data': rewards_data }
            )
        
class CustomerOrderView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client
    def post(self, request):
        #print(request.POST)
        endpoint = self.request.path
        #testing purpose
        print(endpoint)
        email = request.POST.get('email')
        order_total = request.POST.get('order_total')

        #testing purpuso
        #print(email)
        #print(order_total)
        
        try:
            print("try:")
            # Assumes 'submit_order' returns a JSON response
            response = self.rewards_service_client.submit_order(email, order_total)
            #   testing: print("try:after response")
            # Check for successful response or handle accordingly
            if response.status_code == 200:

                return redirect('rewards') 
            else:
                ##need further development
                return redirect('rewards') 
        except:
            ##need further development
            return redirect('rewards') 
            