from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
<<<<<<< HEAD
from django.utils import timezone
from django import forms 

class EmailForm(forms.Form):
    
    email = forms.EmailField(label='Email', required=True, max_length=200, widget=forms.EmailInput(attrs={
        "class": "",
        "placeholder": "Enter your registered email address"
    }))


class ResetPasswordForm(forms.Form):
    
    password = forms.CharField(label='New Password', required=True, max_length=200, widget=forms.PasswordInput(attrs={
            "class": "",
            "placeholder": ""
        }))

    password2 = forms.CharField(label='Confirm New Password', required=True, max_length=200, widget=forms.PasswordInput(attrs={
            "class": "",
            "placeholder": ""
        }))

 
class MySignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    

