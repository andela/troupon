from django.contrib.auth.forms import UserCreationForm
from account.models import Account 
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
    username = forms.CharField(required = True)


    class meta:
        model = Account
        fields = ('id','email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password1','password2',)

        

        def save(self, commit=True):          
          user = super(MySignupForm, self).save(commit=False)
          user.email = self.cleaned_data['email']
          user.first_name = self.cleaned_data['first_name']
          user.last_name = self.cleaned_data['last_name']
          user.username = self.cleaned_data['username']
          user.is_staff = True

          if commit:
            user.save()
          return user

