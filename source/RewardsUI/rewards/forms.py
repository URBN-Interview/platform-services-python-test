from django import forms


class SearchCustomerForm(forms.Form):
    email_address = forms.EmailField(label="Email_Address",max_length=60,required=False)

class CustomerOrderForm(forms.Form):
    email_address = forms.EmailField(label="Email_Address",max_length=60)
    order_total = forms.FloatField(label="Order_Total")
