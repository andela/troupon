from django import forms
from models import UserProfile


class UserProfileForm(forms.ModelForm):
    """This class defines a model form using the 'UserProfile' model.
    """

    class Meta:
	"""This class modifies the UserProfileForm class.

        Attributes:
            model: A model from which to construct the form.
            field: A tuple of the form fields that are fillable.
        """
        model = UserProfile
        fields = ('occupation', 'phonenumber', 'country', 'location')
