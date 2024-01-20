from django import forms
from .models import Vendor # import the Vendor model the field

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']