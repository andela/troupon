from django import forms
from userprofile.models import UserProfile, TrouponMerchant


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'user_state', 'interest')


class TrouponMerchantForm(forms.ModelForm):

    class Meta:
        model= TrouponMerchant
        fields = '__all__'