from django import forms


class DealForm(forms.Form):
    """
    Handles verification of form inputs
    """
    active = forms.BooleanField(label='Is active?', required=False)
    max_quantity_available = forms.CharField(
        label='Max. quantity available', max_length=10
    )
