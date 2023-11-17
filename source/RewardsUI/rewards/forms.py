from django import forms


class UserSearchForm(forms.Form):
    user_email = forms.EmailField(label="User email", max_length=65)


class OrderPostForm(forms.Form):
    order_email = forms.EmailField(label="Order email")
    order_total = forms.FloatField(label="Order total")
