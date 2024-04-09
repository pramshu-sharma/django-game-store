from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(help_text='')
    password = forms.PasswordInput()

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class RegistrationForm(ModelForm):
    username = forms.CharField(help_text='')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'profile_picture', 'first_name', 'last_name', 'email']



