from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name','last_name','phone','email','address_line1','address_line2','country','state','district','city','pincode']

