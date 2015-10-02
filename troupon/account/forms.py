from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class EmailForm(forms.Form):
    
    email = forms.EmailField(label='Email', required=True, max_length=200, widget=forms.EmailInput(attrs={
        "placeholder": "Enter your registered email address.",
        "class": "form-control"
    }))


class ResetPasswordForm(forms.Form):

    password = forms.CharField(label='New Password', max_length=200, widget=forms.PasswordInput())

    password_conf = forms.CharField(label='Confirm New Password', max_length=200, widget=forms.PasswordInput())

    def clean_password_conf(self):
        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')
        if password and password_conf:
            if password != password_conf:
                self.add_error('password_conf', "Password fields must match.")
        return password_conf


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
