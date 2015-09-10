from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class EmailForm(forms.Form):
    
    email = forms.EmailField(label='Email', required=True, max_length=200, widget=forms.EmailInput(attrs={
        "class": "",
        "placeholder": "Enter your registered email address"
    }))


class ResetPasswordForm(forms.Form):
    
    password1 = forms.CharField(label='New Password', max_length=200, widget=forms.PasswordInput())

    password2 = forms.CharField(label='Confirm New Password', max_length=200, widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                self.add_error('password2', "Password fields must match.")
        return password2


class UserSignupForm(UserCreationForm):
    '''
    Field defined to override default field property.
    '''
    email = forms.EmailField(required = True)
    

    class Meta:
        '''
        UserCreationform uses the django User object. 
        ''' 
        model = User
        fields = ('username','email','password1','password2')



    def save(self):
        '''
        Save method used by the AbstractUser object.

        Subclassed by the User object to save data to database and called by UserSignupRequest
        class in accounts/views.py.
        '''
        user = User.objects.create_user(username=self.cleaned_data['username'],email=self.cleaned_data['email'],password=self.cleaned_data['password1'])
        return user
