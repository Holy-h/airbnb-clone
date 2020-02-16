from django import forms
from django.contrib.auth import password_validation
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


class SignupForm(forms.ModelForm):

    """ SignupForm Definition """

    error_messages = {"password_mismatch": "비밀번호가 일치하지 않습니다."}

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"], code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        # 바꿔치기
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        user.username = email
        user.set_password(password1)
        if commit:
            user.save()
        return user
