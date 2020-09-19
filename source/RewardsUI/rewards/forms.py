from django import forms

class FilterForm(forms.Form):
    email = forms.EmailField(required=true)

class OrderForm(forms.Form):
    email = forms.EmailField(required=True)
    total = forms.FloatField(required=True)
