from django import forms


class DealForm(forms.Form):
    """
    Handles verification of form inputs
    """
    active = forms.BooleanField(label='Is active?', required=False)
    quorum = forms.CharField(label='Quorum', max_length=10)
