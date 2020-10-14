from django import forms

class ClientRewardForm(forms.Form):
    email = forms.CharField(label='Email')
    amount = forms.CharField(label='Amount')
