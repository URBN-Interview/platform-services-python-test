from django import forms
from django.core import validators


class SearchUserForm(forms.Form):
    email_address = forms.CharField(label='Enter email address:', max_length=100, required=False,
                                    validators=[validators.EmailValidator])


class SubmitOrderForm(SearchUserForm):
    email_address = forms.CharField(label='Enter email address:', max_length=100,
                                    validators=[validators.EmailValidator])
    order_total = forms.FloatField(label='Enter order total:', min_value=0,
                                   validators=[validators.MinValueValidator])
