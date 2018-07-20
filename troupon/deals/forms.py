from django import forms
from models import Review


class ReviewForm(forms.ModelForm):
    """This class defines a model form using the 'Review' model.
    """

    class Meta:
	"""This class modifies the ReviewForm class.

        Attributes:
            model: A model from which to construct the form.
            field: A tuple of the form fields that are fillable.
        """
        model = Review
        fields = ('description',)
