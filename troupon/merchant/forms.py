from django import forms
from cloudinary.forms import CloudinaryFileField

integerfields = {
            'max_quantity_available': True,
            'original_price': True,
            'quorum': True,
            'current_price': True,
        }


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

    @staticmethod
    def construct_int(value):
        """Contructs an integer value from a string or a comma separated list
        """
        if value == '' or value is None:
            return 0
        print value
        index = value.find(',')
        if index is -1:
            return int(value)
        else:
            return int(value[:index] + value[index+1:])

    def is_valid(self):
        """
        Checks if form data is valid.
        """
        super(DealForm, self).is_valid()
        for key, value in self.data.items():
            if value is None or value == '':
                if key != 'quorum':
                    continue
            if integerfields.get(key, False):
                if type(str(value)) is str:
                    value = DealForm.construct_int(value)
                # remove errors upon normalization of uncleaned data
                self.errors.pop(key, None)
                # update value of cleaned data
                self.cleaned_data[key] = value

        return len(self.errors) is 0

    def save(self, deal):
        """
        Updates information about a deal
        """
        for key, value in self.cleaned_data.items():
            if value is None or value == '':
                # skip the quorum field
                if key != 'quorum':
                    continue
            setattr(deal, key, value)
        deal.save()
