from django import forms


class RewardForm(forms.Form):
    email_address = forms.EmailField(max_length=100, widget=forms.TextInput(
            attrs={'class': 'col', 'name': 'email_address'}
        ))
    amount = forms.IntegerField(widget=forms.TextInput(
            attrs={'class': 'col', 'name': 'amount'}
        ))


class CustomerForm(forms.Form):
    email = forms.EmailField(max_length=100 , widget=forms.TextInput(
            attrs={'class': 'col', 'name': 'email'}
        ))
