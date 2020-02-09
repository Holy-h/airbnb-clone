from django import forms
from . import models


class LoginForm(forms.Form):

    """ LoginForm Definition """

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # https://docs.djangoproject.com/en/3.0/ref/forms/validation/#form-and-field-validation

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is worng"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))
