from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label = "email", max_length = 100)

class OrderForm(forms.Form):
    order_email = forms.EmailField(label="order_email")
    orders = forms.FloatField(label="orders")
