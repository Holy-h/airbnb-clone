from django.views.generic import FormView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):
    """ LoginView Definition """

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "kepy1106@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignupView(FormView):

    """ SignupView Definition """

    template_name = "users/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Byunghun",
        "last_name": "Kim",
        "email": "figma@kakao.com",
    }

    def form_valid(self, form):
        # form이 유효하면 save()
        form.save()

        # save() 이후에 로그인
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            user.verify_email()
        return super().form_valid(form)


def complete_verification(request, secret):
    try:
        user = models.User.objects.get(email_secret=secret)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do: add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# Login
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-in

# LoginView
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
