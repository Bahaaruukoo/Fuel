from email.policy import default
from pyexpat import model
from xml.dom.minidom import Attr
from django import forms
from .models import gas_offer

class SearchForm(forms.Form):
    search = forms.CharField()

class UpdateForm(forms.Form):
    filled_amount = forms.IntegerField()

class PromoCodeForm(forms.ModelForm):
    status= forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked'}))
    class Meta:
        model = gas_offer
        fields = ['plate_number','permited_amount', 'status']
