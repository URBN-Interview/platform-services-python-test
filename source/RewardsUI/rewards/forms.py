from django import forms

class OrderForm(forms.Form):
    user_email = forms.EmailField(label="Email")
    user_order = forms.IntegerField(label="Order")

