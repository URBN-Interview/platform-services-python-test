from django import forms
from django.utils.safestring import mark_safe


class OrderForm(forms.Form):
    email = forms.CharField(max_length=200, label=mark_safe("Enter email address: "), label_suffix="")
    order_total = forms.FloatField(label=mark_safe("<br/><br/>Enter order total: "), min_value=0.0, label_suffix="")


class UserFilterForm(forms.Form):
    email = forms.CharField(max_length=200, label="Email address: ", label_suffix="")
