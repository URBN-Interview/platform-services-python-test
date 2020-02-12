from django import forms


class SearchCustomerForm(forms.Form):
    email_address = forms.CharField(label="Email_Address",max_length=60)

class CustomerOrderForm(forms.Form):
    email_address = forms.CharField(label="Email_Address",max_length=60)
    order_total = forms.FloatField(label="Order Total")