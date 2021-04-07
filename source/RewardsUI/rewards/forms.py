from django import forms

#Using Django to create forms

class OrderForm(forms.Form):
    user_email = forms.EmailField(label="Email")
    user_order = forms.IntegerField(label="Order")

class SearchForm(forms.Form):
    user_email = forms.EmailField(label="Email")

