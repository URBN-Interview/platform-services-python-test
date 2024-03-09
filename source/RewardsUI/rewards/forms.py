from django import forms

class AddRewardsForm(forms.Form):
    """
    A form for adding rewards to a user account.

    This form collects the user's email address and the total amount of rewards to add.
    """

    email = forms.EmailField(label='Email')  # Field for user's email address
    total = forms.FloatField(label='Total')   # Field for total amount of rewards

