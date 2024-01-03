from django import forms
from home.models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'group', 'payment_method','admin']
