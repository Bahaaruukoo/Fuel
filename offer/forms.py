from pyexpat import model
from django import forms
from .models import gas_offer

class SearchForm(forms.Form):
    search = forms.CharField()

class UpdateForm(forms.Form):
    filled = forms.IntegerField()

class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = gas_offer
        fields = ['plate_number','permited_amount', 'status']
