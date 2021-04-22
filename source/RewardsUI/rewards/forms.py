from django import forms


class orderDetail(forms.Form):
    emailAddress = forms.CharField(label='emailAddress', max_length=100)
    total = forms.CharField(label='total', max_length=100)


class customerDetail(forms.Form):
    emailAddress = forms.CharField(label='emailAddress', max_length=100)
