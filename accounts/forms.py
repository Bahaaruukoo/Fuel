from dataclasses import field, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class CashierRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gasstation', 'role']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UpdateUser(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateMyCachier(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email']

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gasstation' ]
