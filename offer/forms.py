from dataclasses import fields
from email.policy import default
from logging import PlaceHolder
from pyexpat import model
from tkinter import Widget
from xml.dom.minidom import Attr
from django import forms
from .models import Audited, Gas_offer, Gasstation, log_table

class SearchForm(forms.Form):
    search = forms.CharField()

class UpdateForm(forms.Form):
    filled_amount = forms.IntegerField()

class PromoCodeForm(forms.ModelForm):
    status= forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked' : 'checked'}))
    class Meta:
        model = Gas_offer
        fields = ['plate_number','permited_amount', 'fuel', 'status']

class AuditForm(forms.ModelForm):
    start_date = forms.DateField()#widget=forms.TextInput())#attrs={ "id":"startDate"} ))
    end_date = forms.DateField()#widget=forms.DateInput(attrs={ "id":"endDate"} ))

    class Meta:
        model = log_table
        fields = ['gasstation']

class PaymentForm(forms.ModelForm):
    money_reciever = forms.CharField(widget=forms.Textarea(attrs={"rows":5 , "id":"money", "placeholder":"Full Informatin upto 250 character"}, ))
    class Meta:
        model=Audited
        fields = ['money_reciever']