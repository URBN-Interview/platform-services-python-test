from django import forms


class SearchUserForm(forms.Form):
    email_address = forms.CharField(label="Email Address", max_length=50)


class AddOrderForm(forms.Form):
    email_address_order = forms.CharField(label="Email Address", max_length=50)
    order_total = forms.FloatField(label="Order Total")
