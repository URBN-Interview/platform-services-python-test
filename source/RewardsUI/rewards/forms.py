from django import forms


class NewPurchaseForm(forms.Form):
    email = forms.EmailField(required=True)
    order = forms.FloatField(required=True)


class EmailLookupForm(forms.Form):
    email = forms.EmailField(required=True)
