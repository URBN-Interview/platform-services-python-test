from django import forms


class AddOrderForm(forms.Form):
    emailAddress = forms.EmailField(label='Enter email')
    orderTotal = forms.FloatField(label='Enter order Total')


class QueryUser(forms.Form):
    searchEmailAddress = forms.EmailField(label='Enter email', required=False)