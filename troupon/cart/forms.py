from django import forms
from models import UserShippingDetails


class ShippingForm(forms.ModelForm):
    """This class defines a model form using the 'UserShippingDetails' model.
    """

    class Meta:
        model = UserShippingDetails
        fields = ('street', 'postal', 'state', 'telephone')
