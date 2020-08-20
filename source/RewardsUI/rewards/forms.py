from django import forms

class AddOrder(forms.Form):
    email_address = forms.CharField(label="Email", required = True)
    order_total = forms.FloatField(label="Order Total", required = True)


class Search(forms.Form):
    email_address = forms.CharField(label="Email", required=True) 
