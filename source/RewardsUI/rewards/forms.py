from django import forms

class EmailFilterForm(forms.Form):
    email_filter = forms.EmailField(label='email', max_length=100)