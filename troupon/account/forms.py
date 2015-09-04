from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django import forms 


class MySignupForm(UserCreationForm):
    email = forms.EmailField(required = True)
    username = forms.CharField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)




    class meta:        
        fields = ('email', 'username','password1','password2','first_name', 'last_name')

        
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

