"""Form structures for authentication."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EmailForm(forms.Form):
    """Class which specifies structure of the reset password email form.

    Atrributes:
              email

    """

    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your registered email address."
            }
        )
    )


class ResetPasswordForm(forms.Form):
    """Class that defines the structure of the reset password form.

    Attributes:
              password,
              password_conf,
    """

    password = forms.CharField(
        label='New Password',
        max_length=200,
        widget=forms.PasswordInput()
    )

    password_conf = forms.CharField(
        label='Confirm New Password',
        max_length=200,
        widget=forms.PasswordInput()
    )

    def clean_password_conf(self):
        """Check if password matches the confirmation password.

        Returns:
                password_conf: The cleaned confirmation password
        Raises:
               password fields must match error
        """
        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')
        if password and password_conf:
            if password != password_conf:
                self.add_error('password_conf', 'Password fields must match.')
        return password_conf


class UserSignupForm(UserCreationForm):
    """Field defined to override default field property."""

    email = forms.EmailField(required=True)

    class Meta:
        """UserCreationform uses the django User object."""

        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        """Save method used by the AbstractUser object.

        Subclassed by the User object to save data to database and
        called by UserSignupRequest class in accounts/views.py.

        Arguments:
                 commit: A flag set to True

        Returns:
               saved user object
        """
        user = super(UserSignupForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.is_active = False

        if commit:
            user.save()
        return user
