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

    password2 = forms.CharField(label='Confirm New Password', required=True, max_length=200, widget=forms.PasswordInput(attrs={
            "class": "",
            "placeholder": ""
        }))

class MySignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    username = forms.CharField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)


<<<<<<< HEAD
    class meta:
        model = Account
        fields = ('id','email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password1','password2',)

        
=======


<<<<<<< HEAD
    class meta:
        model = Account
        fields = ('id','email', 'username','password1','password2','first_name', 'last_name')
>>>>>>> [#102560626] code refactor
=======
    class meta:        
        fields = ('email', 'username','password1','password2','first_name', 'last_name')
>>>>>>> [#102560626] changed user object to User.. Major change to forms.py removed Account Model Model now User in forms.py Meta Class

        
        def save(self, commit=True):
            user = super(MySignupForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.is_active = False
            

            if commit:
                user.save()
            return user

