from django import forms
from . import models


class LoginForm(forms.Form):

    """ LoginForm Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # https://docs.djangoproject.com/en/3.0/ref/forms/validation/#form-and-field-validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User does not exist")

    def clean_password(self):
        print("clean password")
        return "password"
