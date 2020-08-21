from django import forms

class Search(forms.Form):
    emailAddress = forms.EmailField(label="Email", required=False) 

class AddOrder(forms.Form):
    emailAddress = forms.EmailField(label="Email", required = True)
    orderTotal = forms.FloatField(label="Order Total", required = True)