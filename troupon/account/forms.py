from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
 
class UserSignupForm(UserCreationForm):
    '''
    Fields defined to override default field property.
    '''
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required=True)


    class Meta:
        '''
        UserCreationform uses the django User object. 
        ''' 
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')



    def save(self):
        '''
        Save method used by the AbstractUser object.

        Subclassed by the User object to save data to database and called by UserSignupRequest
        class in accounts/views.py.
        '''
        user = User.objects.create_user(username=self.cleaned_data['username'],email=self.cleaned_data['email'],password=self.cleaned_data['password1'])
        return user
