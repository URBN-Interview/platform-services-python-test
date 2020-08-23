from django import forms


class OrderForm(forms.Form):
    email_address = forms.CharField(max_length=100)
    order_total = forms.FloatField()


class UserForm(forms.Form):
    email_address = forms.CharField(max_length=100)
