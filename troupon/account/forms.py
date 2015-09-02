from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=200, widget=forms.TextInput(attrs={
            "class": "",
            "placeholder": "Enter your registered email address"
        }))