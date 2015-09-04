from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
    class meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')

    password2 = forms.CharField(label='Confirm New Password', required=True, max_length=200, widget=forms.PasswordInput(attrs={
            "class": "",
            "placeholder": ""
        }))

 
class MySignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'],email=self.cleaned_data['email'],password=self.cleaned_data['password1'])
        return user
