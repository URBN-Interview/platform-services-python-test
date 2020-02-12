from django import forms

# using EmailField will validate the email input for us when it is entered
class SearchCustomerForm(forms.Form):
    email_address = forms.EmailField(label="Email_Address",max_length=60,required=False)

class CustomerOrderForm(forms.Form):
    email_address = forms.EmailField(label="Email_Address",max_length=60)
    order_total = forms.FloatField(label="Order_Total")
