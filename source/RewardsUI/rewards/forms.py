from django import forms


class SearchUserForm(forms.Form):
    email_address = forms.CharField(label="Email Address", max_length=50)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SearchUserForm, self).__init__(*args, **kwargs)
