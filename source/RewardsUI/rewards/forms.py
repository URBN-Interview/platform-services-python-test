from django import forms

class AddRewardsForm(forms.Form):
    email = forms.EmailField()
    total = forms.FloatField()

