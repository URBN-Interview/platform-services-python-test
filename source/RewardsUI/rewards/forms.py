from django import forms


class AddOrderForm(forms.Form):
    email_address = forms.EmailField(required=True, label="Email address")
    order_total = forms.DecimalField(decimal_places=2, required=True, label="Order total")
