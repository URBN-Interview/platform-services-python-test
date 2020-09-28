from django import forms

class AddOrder(forms.Form):
    email = forms.EmailField(label = 'Email:')
    orderTotal = forms.FloatField(label = 'Order Total:')

class QueryUser(forms.Form):
    email = forms.EmailField(label = 'Email:')
    orderTotal = forms.FloatField(label = 'Order Total:')