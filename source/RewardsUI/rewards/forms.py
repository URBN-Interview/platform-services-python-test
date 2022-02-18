# RewardUI Forms
# forms classes and descriptions

from django import forms

# CustomerOrder form
# email and total for orders
class CustomerOrder(forms.Form):
    email = forms.EmailField(label="Enter email address: ")
    total = forms.FloatField(label="Enter order total: ")