from django import forms
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm
 
class MySignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required=True)


    class meta:
        model = AbstractUser
        fields = ('first_name','last_name','username','email','password1','password2')



    def save(self, commit=True):
        user = super(MySignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = True 

        if commit:
            user.save()
        return user

