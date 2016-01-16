from django import forms
from cloudinary.forms import CloudinaryFileField


class DealForm(forms.Form):
    """
    Handles verification of form inputs
    """
    active = forms.BooleanField(label='Is active?', required=False)
    current_price = forms.IntegerField(label='Current price', required=False)
    max_quantity_available = forms.IntegerField(
        label='Max. quantity available', required=False
    )
    original_price = forms.IntegerField(label='Original price', required=False)
    image = CloudinaryFileField(required=False)
    quorum = forms.IntegerField(label='Quorum', required=False)
    title = forms.CharField(label='Title', required=False, max_length=200)
    address = forms.CharField(label='Address', required=False, max_length=200)

    def save(self, deal):
        """
        Updates information about a deal
        """
        integerfields = {
            'max_quantity_available': True,
            'original_price': True,
            'quorum': True,
            'current_price': True,
        }
        for key, value in self.cleaned_data.items():
            if value is None or value == '':
                if key != 'quorum':
                    continue
            if integerfields.get(key, False):
                value = 0 if value is None else int(value)
            setattr(deal, key, value)
        deal.save()
