from django import forms
from django.core import validators

class GetCustomer(forms.Form):
    email = forms.EmailField(label = "Email address", max_length=50, required=True, validators=[validators.validate_email,],
                widget=forms.TextInput(attrs={'id': 'search_email',
                    'placeholder': 'xxx@xx.xx',
                    'oninvalid':'this.setCustomValidity("Email address is required")'}))

class CustomerOrder(forms.Form):
    email = forms.EmailField(label = "Email address", max_length=50, required=True,
                widget=forms.TextInput(attrs={'id': 'customer_email', 'placeholder': 'xxx@xx.xx',
                    'oninvalid':'this.setCustomValidity("Email address is required")'}))
    orderTotal = forms.FloatField(label = "Enter order total", min_value=0, required=True,
                widget=forms.TextInput(attrs={'id': 'order_total', 'placeholder': 'enter your order total',
                    'oninvalid':'this.setCustomValidity("Order total is required")'}))