from django import forms


class OrderForm(forms.Form):
    email = forms.CharField(max_length=200, label="Enter email address")
    order_total = forms.FloatField(label="Enter order total", min_value=0.0)


class UserFilterForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email address")
