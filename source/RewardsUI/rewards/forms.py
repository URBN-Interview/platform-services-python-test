from django import forms

class EmailFilterForm(forms.Form):
    email_filter = forms.CharField(label='email', max_length=100)


class PostOrderForm(forms.Form):
    email = forms.CharField(label='email')
    total = forms.CharField(label='order_total')