from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(label='Enter email address')
    amount = forms.IntegerField(label='Enter order total')


class SearchForm(forms.Form):
    email = forms.EmailField(label='Enter email address', required=False)