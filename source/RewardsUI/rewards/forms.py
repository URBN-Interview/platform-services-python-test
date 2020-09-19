from django import forms

class OrderForm(forms.Form):
    email = forms.EmailField(required=True)
    total = forms.FloatField(required=True)
