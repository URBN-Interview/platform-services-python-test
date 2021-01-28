from django import forms


class RewardForm(forms.Form):
    email_address = forms.EmailField(max_length=100)
    amount = forms.DecimalField(max_digits=5)


class CustomerForm(forms.Form):
    email = forms.EmailField(max_length=100)
