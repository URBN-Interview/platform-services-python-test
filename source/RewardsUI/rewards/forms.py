from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label='email')

class OrderForm(forms.Form):
    order_email = forms.CharField(label="order email")
    order_total = forms.CharField(label="order total")