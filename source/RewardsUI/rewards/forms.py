from django import forms


class OrderForm(forms.Form):
    email = forms.EmailField(label='Enter email address:', required=True)
    order_total = forms.FloatField(label='Enter order total:', required=True)


class UserRewardsForm(forms.Form):
    email_filter = forms.EmailField(label='Email address:', required=True)
