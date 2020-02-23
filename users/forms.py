from django import forms
from django.contrib.auth import password_validation
from . import models


class LoginForm(forms.Form):

    """ LoginForm Definition """

    error_messages = {
        "password_mismatch": "비밀번호가 일치하지 않습니다.",
        "user_does_not_exist": "존재하지 않는 이메일입니다.",
    }

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "이메일"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    # https://docs.djangoproject.com/en/3.0/ref/forms/validation/#form-and-field-validation

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error(
                    "password",
                    forms.ValidationError(
                        self.error_messages["password_mismatch"],
                        code="password_mismatch",
                    ),
                )
        except models.User.DoesNotExist:
            self.add_error(
                "email",
                forms.ValidationError(
                    self.error_messages["user_does_not_exist"],
                    code="user_does_not_exist",
                ),
            )


class SignupForm(forms.ModelForm):

    """ SignupForm Definition """

    error_messages = {
        "password_mismatch": "비밀번호가 일치하지 않습니다.",
        "existing_user": "이미 존재하는 이메일입니다.",
    }

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "이름"}),
            "last_name": forms.TextInput(attrs={"placeholder": "성"}),
            "email": forms.TextInput(attrs={"placeholder": "이메일"}),
        }

    password1 = forms.CharField(
        label="비밀번호", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )
    password2 = forms.CharField(
        label="비밀번호 확인", widget=forms.PasswordInput(attrs={"placeholder": "비밀번호 확인"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            self.add_error(
                "email",
                forms.ValidationError(
                    self.error_messages["existing_user"], code="existing_user"
                ),
            )
        except models.User.DoesNotExist:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                forms.ValidationError(
                    self.error_messages["password_mismatch"], code="password_mismatch",
                ),
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
