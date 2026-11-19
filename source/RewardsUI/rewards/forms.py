from decimal import Decimal

from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=254)
    order_total = forms.DecimalField(
        label="Order total ($)", min_value=Decimal("0"), max_digits=12, decimal_places=2,
    )


class CustomerSearchForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=254, required=False)
