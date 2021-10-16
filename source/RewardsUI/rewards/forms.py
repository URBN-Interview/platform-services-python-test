from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email 

import re

class CustomerOrderForm(forms.Form):
    customer_email_address = forms.CharField(label='Enter Email Address', max_length=100, validators=[validate_email])
    customer_order = forms.FloatField(label='Enter Order Total')

class CustomerRewardForm(forms.Form):
    customer_email_address = forms.CharField(label='Enter Email Address', max_length=100, validators=[validate_email])    