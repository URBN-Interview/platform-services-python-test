import logging

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from rewards.clients.rewards_service_client import RewardsServiceClient

#imports for messages, redirect and render
from django.contrib import messages
from django.shortcuts import redirect, render

class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__), rewards_service_client=RewardsServiceClient()):
        self.logger = logger
        self.rewards_service_client = rewards_service_client

    def get(self, request):
        endpoint = self.request.path
        print(endpoint)
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
        print(email)

        if email:
            #try:
                customer_rewards_data = self.rewards_service_client.get_customer_rewards(email)
                print(endpoint)
                print("Customer")
                ### Get rewards a user can earn ###
                rewards_data = self.rewards_service_client.get_rewards() 
                #if rewards_data.status_code == 200:
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'customer_rewards_data': customer_rewards_data,'rewards_data': rewards_data }
                )
                #else:
                #    print("Error. This is not rendered yet.")
            # except:
            #     messages.error(request, 'Invalid search. Please try again.')
            #     return render(request, self.template_name)

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

        print(email)
        print(order_total)

        try:
            # Assumes 'submit_order' returns a JSON response
            response = self.rewards_service_client.submit_order(email, order_total)
        
            # Check for successful response or handle accordingly
            if response.status_code == 200:
                # Add a success message
                messages.success(request, 'Order submitted successfully!')
                return redirect('rewards')  # Redirect to success page
            else:
                # If the submission fails, display an error message
                messages.error(request, 'Failed to submit order. Please try again.')
                # Render the same page with an error message
                return render(request, self.template_name)
        except:
            # If the submission invalidates, display an error message
            messages.error(request, 'Invalid submit order request. Please try again.')
            # Render the same page with an error message
            return render(request, self.template_name)
            
            