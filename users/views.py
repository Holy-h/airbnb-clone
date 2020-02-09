from django.views.generic import FormView
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms


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


# class LoginView(View):
#     """ LoginView Definition """

#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "kepy1106@gmail.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


# Login
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#how-to-log-a-user-in

# LoginView
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#all-authentication-views
