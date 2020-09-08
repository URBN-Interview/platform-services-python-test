from django import forms	

class EmailForm(forms.Form):	
    email = forms.EmailField(label='email')	

class OrderForm(forms.Form):	
    order_email = forms.EmailField(label="order email")	
    order_total = forms.FloatField(label="order total")