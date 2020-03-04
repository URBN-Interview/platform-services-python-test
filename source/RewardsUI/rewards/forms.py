from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label='email')

class OrderForm(forms.Form):
    email = forms.CharField(label="email")
    totalOrder = forms.CharField(label="totalOrder")