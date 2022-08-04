from django import forms

class OrdersForm(forms.Form):
    email_address = forms.EmailField(label="Enter email address")
    order_total = forms.FloatField(label="Enter order total")