from django import forms


class NewPurchaseForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'email-on-purchase-add', 'name': 'email-on-purchase-add'}))
    email.label = 'Enter email address:'
    order = forms.FloatField(required=True)
    order.label = 'Enter order total:'


class EmailLookupForm(forms.Form):
    email = forms.EmailField(required=True)
    email.label = 'Enter Email:'
