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
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required = True)


    class meta:
        model = Account
        fields = ('email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password','confirm_password',)

        created_at = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

        updated_at = forms.DateTimeField(widget=forms.TextInput(attrs={'readonly':'readonly'}))


        def save(self, commit=True):          
          user = super(MySignupForm, self).save(commit=False)
          user.email = self.cleaned_data['email']
          user.first_name = self.cleaned_data['first_name']
          user.last_name = self.cleaned_data['last_name']
          user.username = self.cleaned_data['username']


          if commit:
            Account.objects.create_user(email = user.email,password = password)
            user.save()
          return user


