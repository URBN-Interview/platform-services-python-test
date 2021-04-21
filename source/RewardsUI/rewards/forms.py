from django import forms

class EmailForm(forms.Form):
    email = forms.CharField(label ="email", max_length = 200)

class OrderForm(forms.Form):
    orderEmail = forms.EmailField(label="orderEmail")
    points = forms.FloatField(label="points")